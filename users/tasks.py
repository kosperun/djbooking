from django.conf import settings

from config.celery import app as celery_app
from shared.email_service import EmailService


@celery_app.task
def send_confirmation_link(email: str, security_token: str):
    link = f"{settings.DOMAIN}/sign-up?token={security_token}&email={email}"
    return EmailService.send_confirmation_link(email=email, link=link)
