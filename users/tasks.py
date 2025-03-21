from urllib.parse import urlencode

from django.conf import settings

from config.celery import app as celery_app
from shared.email_service import EmailService
from users.selectors import user_delete_by_id


@celery_app.task
def send_confirmation_link_task(email: str, security_token: str):
    params = {"email": email, "token": security_token}
    link = f"{settings.DOMAIN}/sign-up?{urlencode(params)}"
    EmailService.send_confirmation_link(email=email, link=link)


@celery_app.task
def send_change_password_link_task(email: str, security_token: str):
    params = {"email": email, "token": security_token}
    link = f"{settings.DOMAIN}/change-password?{urlencode(params)}"
    return EmailService.send_change_password_link(email=email, link=link)


@celery_app.task
def send_change_email_link_task(new_email: str, security_token: str):
    params = {"email": new_email, "token": security_token}
    link = f"{settings.DOMAIN}/change-email?{urlencode(params)}"
    return EmailService.send_change_email_link(email=new_email, link=link)


@celery_app.task
def delete_unregistered_user_after_security_token_expired(user_id: str):
    user_delete_by_id(user_id)
