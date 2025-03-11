from uuid import UUID

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now, timedelta

from shared.exceptions import DjBookingAPIError
from users.exceptions import RegistrationTimePassed
from users.models import User as UserModel
from users.selectors import get_user_by_id_and_security_token
from users.tasks import delete_unregistered_user_after_security_token_expired, send_confirmation_link

User = get_user_model()


def user_create(**kwargs) -> UserModel:
    password = kwargs.pop("password")
    user = User(**kwargs)
    validate_password(password, user)
    user.set_password(password)
    user.security_token_expiration_time = now() + timedelta(hours=settings.SECURITY_TOKEN_LIFE_TIME_IN_HOURS)
    user.save()
    send_confirmation_link.delay(user.email, user.security_token)
    return user


def confirm_registration(user_id: UUID, security_token: UUID) -> UserModel:
    user = get_user_by_id_and_security_token(user_id, security_token)

    if user.security_token_expiration_time < now():
        delete_unregistered_user_after_security_token_expired.delay(str(user_id))
        raise RegistrationTimePassed()

    user.security_token = ""
    user.is_active = True
    user.save()
    return user


def change_password(user: UserModel, old_password: str, new_password: str) -> UserModel:
    if not user.check_password(old_password):
        raise DjBookingAPIError("Wrong password!")
    user.set_password(new_password)
    user.save()
    return user
