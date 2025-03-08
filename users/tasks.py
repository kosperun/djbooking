from urllib.parse import urlencode

from django.conf import settings

from config.celery import app as celery_app
from shared.email_service import EmailService


@celery_app.task
def send_confirmation_link(email: str, security_token: str):
    params = {"email": email, "token": security_token}
    link = f"{settings.DOMAIN}/sign-up?{urlencode(params)}"
    return EmailService.send_confirmation_link(email=email, link=link)
