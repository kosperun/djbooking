from config.celery import app as celery_app
from shared.email_service import EmailService


@celery_app.task
def send_booking_confirmation_email_to_user(booking_id: str):
    return EmailService.send_booking_confirmation_email_to_user(booking_id)


@celery_app.task
def send_booking_confirmation_email_to_owner(booking_id: str):
    return EmailService.send_booking_confirmation_email_to_owner(booking_id)


@celery_app.task
def send_booking_cancellation_email_to_owner(booking_id: str):
    return EmailService.send_booking_cancellation_email_to_owner(booking_id)


@celery_app.task
def send_booking_cancellation_email_to_user(booking_id: str):
    return EmailService.send_booking_cancellation_email_to_user(booking_id)


@celery_app.task
def delete_expired_unpaid_booking(booking_id: str):
    from bookings.services import booking_delete

    booking_delete(booking_id)
