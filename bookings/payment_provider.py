from decimal import Decimal
from uuid import UUID

import stripe
from django.conf import settings
from djstripe import webhooks

from bookings.exceptions import PaymentProviderException
from bookings.services import booking_confirm

stripe.api_key = settings.STRIPE_API_KEY


def create_payment_user_with_email(email: str) -> stripe.Customer:
    """Create a stripe customer."""
    try:
        return stripe.Customer.create(email=email)
    except stripe.InvalidRequestError as exc:
        raise PaymentProviderException(message=exc.user_message) from exc


def create_payment_intent(
    customer_id: str | UUID,
    amount: Decimal,
    currency: str,
    metadata: dict,
    capture_method: str,
    receipt_email: str,
) -> stripe.PaymentIntent:
    amount_in_cents = int(amount * 100)
    try:
        return stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            customer=customer_id,
            capture_method=capture_method,
            metadata=metadata,
            receipt_email=receipt_email,
        )
    except stripe.InvalidRequestError as exc:
        raise PaymentProviderException(message=exc.user_message) from exc


def get_payment_intent(payment_intent_id: str) -> stripe.PaymentIntent:
    try:
        return stripe.PaymentIntent.retrieve(id=payment_intent_id)
    except stripe.InvalidRequestError as exc:
        raise PaymentProviderException(message=exc.user_message) from exc


def create_refund(
    payment_intent_id: str,
    amount: Decimal,
    metadata: dict,
) -> stripe.Refund:
    amount_in_cents = int(amount * 100)
    try:
        return stripe.Refund.create(payment_intent=payment_intent_id, amount=amount_in_cents, metadata=metadata)
    except stripe.InvalidRequestError as exc:
        raise PaymentProviderException(message=exc.user_message) from exc


@webhooks.handler("payment_intent.succeeded")
def confirm_payment(event, **kwargs):
    """Change booking status to 'PAID'"""

    payment_intent = event.data["object"]
    booking_confirm(payment_intent["metadata"])
