from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now, timedelta
from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as Fake
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

fake = Fake()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    password = make_password(fake.password())
    date_of_birth = Faker("date")
    is_active = True
    security_token = uuid4()
    security_token_expiration_time = now() + timedelta(minutes=15)

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override _create method to save the hashed password into the DB
        instead of the default plain text password
        """
        password = kwargs.get("password", None)
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        return obj


@pytest.fixture
def authenticate_user():
    def _authenticate(user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return client

    return _authenticate
