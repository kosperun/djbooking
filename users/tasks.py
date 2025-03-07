from django.conf import settings
from django.utils.module_loading import import_string

from config.celery import app as celery_app

email_provider = import_string(settings.EMAIL_PROVIDER)


@celery_app.task
def send_confirmation_link(email: str, security_token: str):
    link = f"{settings.DOMAIN}/sign-up?token={security_token}&email={email}"
    return email_provider.send_confirmation_link(email=email, link=link)
