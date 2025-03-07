# from uuid import UUID, uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now, timedelta

from users.models import User as UserModel
from users.tasks import send_confirmation_link

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
