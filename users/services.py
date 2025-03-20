from uuid import UUID, uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now, timedelta

from shared.exceptions import DjBookingAPIError
from users.exceptions import RegistrationTimePassed
from users.models import PaymentUser
from users.models import User as UserModel
from users.selectors import (
    get_user_by_email,
    get_user_by_id_and_security_token,
    get_user_by_security_token,
    get_user_by_security_token_and_email,
)
from users.tasks import (
    delete_unregistered_user_after_security_token_expired,
    send_change_email_link_task,
    send_change_password_link_task,
    send_confirmation_link_task,
)

User = get_user_model()


def user_create(**kwargs) -> UserModel:
    password = kwargs.pop("password")
    user = User(**kwargs)
    validate_password(password, user)
    user.set_password(password)
    user.security_token_expiration_time = now() + timedelta(hours=settings.SECURITY_TOKEN_LIFE_TIME_IN_HOURS)
    user.save()
    send_confirmation_link_task.delay(user.email, user.security_token)
    return user


def confirm_registration(user_id: UUID, security_token: UUID) -> UserModel:
    from payments.services import create_stripe_customer_with_email

    user = get_user_by_id_and_security_token(user_id, security_token)

    if user.security_token_expiration_time < now():
        delete_unregistered_user_after_security_token_expired.delay(str(user_id))
        raise RegistrationTimePassed()

    user.security_token = ""
    user.is_active = True
    user.save()
    payment_customer = create_stripe_customer_with_email(email=user.email)
    PaymentUser.objects.create(user=user, customer_id=payment_customer.id)
    return user


def change_password(user: UserModel, old_password: str, new_password: str) -> UserModel:
    if not user.check_password(old_password):
        raise DjBookingAPIError("Wrong password!")
    user.set_password(new_password)
    user.save()
    return user


def send_forgot_password_link(email: str) -> None:
    user = get_user_by_email(email)
    security_token = uuid4()
    user.security_token = security_token
    user.save()
    send_change_password_link_task.delay(user.email, str(security_token))


def confirm_reset_password(security_token: UUID, email: str, new_password: str) -> None:
    user = get_user_by_security_token_and_email(security_token, email)
    user.security_token = ""
    user.set_password(new_password)
    user.save()


def send_change_email_link(user: UserModel, new_email: str) -> None:
    security_token = uuid4()
    user.security_token = security_token
    user.save()
    user.refresh_from_db()
    send_change_email_link_task.delay(new_email, str(security_token))


def change_email(security_token: UUID, new_email: str) -> None:
    user = get_user_by_security_token(security_token)
    user.email = new_email
    user.security_token = ""
    user.save()


def update_user(user: UserModel, **kwargs) -> UserModel:
    for field, value in kwargs.items():
        setattr(user, field, value)
    user.save()
    return user
