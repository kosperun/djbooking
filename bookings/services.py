from datetime import date
from uuid import UUID

from django.conf import settings
from django.utils.timezone import now, timedelta

from bookings.exceptions import EndDateBeforeStartDateError, PastDateError, PropertyAlreadyBookedError
from bookings.models import Booking
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
