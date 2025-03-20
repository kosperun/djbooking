from datetime import date
from typing import Union
from uuid import UUID

from django.conf import settings
from django.utils.timezone import now, timedelta
from rest_framework.exceptions import PermissionDenied

from bookings.exceptions import (
    BookingCannotBeCanceledError,
    EndDateBeforeStartDateError,
    PastDateError,
    PropertyAlreadyBookedError,
)
from bookings.models import Booking
from bookings.selectors import booking_retrieve
from bookings.tasks import (
    delete_expired_unpaid_booking,
    send_booking_cancellation_email_to_owner,
    send_booking_cancellation_email_to_user,
    send_booking_confirmation_email_to_owner,
    send_booking_confirmation_email_to_user,
)
from payments.exceptions import PaymentExpirationTimePassed, PaymentsUserMissingError
from properties.selectors import property_retrieve
from users.models import User


def booking_create(user: User, property_id: UUID, date_from: date, date_to: date) -> Booking:
    current_date = now().date()
    if date_from >= date_to:
        raise EndDateBeforeStartDateError()
    if date_from < current_date or date_to < current_date:
        raise PastDateError()

    property = property_retrieve(property_id)
    if (
        property.bookings.exclude(status=Booking.Status.CANCELED)
        .filter(
            date_from__lt=date_to,
            date_to__gt=date_from,
        )
        .exists()
    ):
        raise PropertyAlreadyBookedError()

    booking = Booking(
        property=property,
        user=user,
        date_from=date_from,
        date_to=date_to,
        payment_expiration_time=now() + timedelta(minutes=settings.BOOKING_PAYMENT_EXPIRATION_TIME_IN_MINUTES),
    )
    booking.save()
    return booking


def booking_pay(user, booking_id: UUID, currency: str = "usd", capture_method: str = "automatic") -> str:
    """Pay for booking if booking is valid.

    Raises:
        PermissionDenied: If payment is attempted by another user different from
        the user who created booking.
    PaymentExpirationTimePassed: If the time for payment has passed.
    """
    from payments.services import create_payment_intent

    booking = booking_retrieve(booking_id)
    _validate_booking_for_payment(booking, user)

    metadata = {"booking_id": str(booking.id)}
    payment_intent = create_payment_intent(
        customer_id=user.payment_user.customer_id,
        amount=booking.property.price,
        currency=currency,
        metadata=metadata,
        capture_method=capture_method,
        receipt_email=user.email,
    )
    booking.payment_intent_id = payment_intent.id
    booking.save()
    return payment_intent.client_secret


def _validate_booking_for_payment(booking: Booking, user: User) -> None:
    if not hasattr(user, "payment_user"):
        raise PaymentsUserMissingError()
    if user != booking.user:
        raise PermissionDenied()
    if booking.payment_expiration_time < now():
        delete_expired_unpaid_booking.delay(str(booking.id))
        raise PaymentExpirationTimePassed()


def booking_confirm(metadata: dict) -> None:
    """Change booking status to "PAID" after successful payment."""
    booking = booking_retrieve(metadata["booking_id"])
    booking.status = Booking.Status.PAID
    booking.save()
    send_booking_confirmation_email_to_user.delay(str(booking.id))
    send_booking_confirmation_email_to_owner.delay(str(booking.id))


def booking_cancel(user: User, booking_id: UUID) -> Booking:
    """Cancel a paid booking by the same user who created it.

    Raises:
        PermissionDenied: If user is not the same who created booking.
        BookingCannotBeCanceledError: If booking has not been paid for or has already been canceled
    """
    from payments.services import create_refund

    booking = booking_retrieve(booking_id)
    _validate_booking_for_cancellation(user, booking)

    create_refund(
        payment_intent_id=booking.payment_intent_id,
        amount=booking.lodging.price,
        metadata={"booking_id": booking.id},
    )
    booking.status = Booking.Status.CANCELED
    booking.save()
    send_booking_cancellation_email_to_owner.delay(str(booking.id))
    send_booking_cancellation_email_to_user.delay(str(booking.id))
    return booking


def _validate_booking_for_cancellation(user: User, booking: Booking) -> Booking:
    if user != booking.user:
        raise PermissionDenied()
    if booking.status != Booking.Status.PAID:
        raise BookingCannotBeCanceledError()


def booking_delete(booking_id: Union[UUID, str]) -> tuple:
    booking = booking_retrieve(booking_id)
    return booking.delete()
