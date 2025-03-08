from django.contrib.auth import get_user_model

from users.exceptions import UserDoesNotExist
from users.models import User as UserModel

User = get_user_model()


def get_user_by_security_token_and_email(security_token: str, email: str) -> UserModel:
    try:
        user = User.objects.get(security_token=security_token, email=email)
    except User.DoesNotExist:
        raise UserDoesNotExist()
    return user
