from bookings.services import booking_confirm
from config.celery import app


@app.task
def confirm_payment(payment_intent):
    """Change booking status to 'PAID'"""

    booking_confirm(payment_intent["metadata"])
