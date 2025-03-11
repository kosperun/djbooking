from uuid import UUID

from django.contrib.auth import get_user_model

from users.exceptions import UserDoesNotExist
from users.models import User as UserModel

User = get_user_model()


def get_user_by_email(email: str) -> UserModel:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise UserDoesNotExist()


def get_user_by_security_token_and_email(security_token: UUID | str, email: str) -> UserModel:
    try:
        user = User.objects.get(security_token=security_token, email=email)
    except User.DoesNotExist:
        raise UserDoesNotExist()
    return user


def get_user_by_id_and_security_token(user_id: UUID | str, security_token: UUID | str) -> UserModel:
    try:
        user = User.objects.get(id=user_id, security_token=security_token)
    except User.DoesNotExist:
        raise UserDoesNotExist()
    return user


def user_delete_by_id(user_id: UUID | str) -> tuple:
    user = User.objects.get(id=user_id)
    return user.delete()
