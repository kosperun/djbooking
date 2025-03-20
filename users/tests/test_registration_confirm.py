from uuid import uuid4

import pytest
from django.utils.timezone import now, timedelta
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from conftest import UserFactory
from payments.models import PaymentUser
from users.exceptions import RegistrationTimePassed, UserDoesNotExist

fake = Faker()


@pytest.mark.django_db
class TestUserRegistrationConfirmAPIView:
    url = reverse("users:registration-confirm")  # POST /api/users/registration/

    def make_assertions(self, user):
        user.refresh_from_db()
        assert user.is_active is False
        assert user.security_token != ""

    def test_confirm_registration_succeeds(self, api_client, mocker):
        security_token_expiration_time = now() + timedelta(hours=2)
        user = UserFactory(is_active=False, security_token_expiration_time=security_token_expiration_time)

        mock = mocker.patch(
            "users.services.create_stripe_customer_with_email", return_value=mocker.MagicMock(id="customer_id")
        )

        payload = {"user_id": user.id, "security_token": user.security_token}
        response = api_client.post(self.url, payload)
        assert response.status_code == HTTP_200_OK
        assert response.data is None

        mock.assert_called_once_with(email=user.email)

        user.refresh_from_db()
        assert user.is_active is True
        assert user.security_token == ""

        payment_user = PaymentUser.objects.first()
        assert payment_user.user == user

    def test_confirm_registration_without_security_token_fails(self, api_client):
        user = UserFactory(is_active=False)

        payload = {"security_token": ""}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "This field is required." in response.data["user_id"]
        assert "Must be a valid UUID." in response.data["security_token"]
        self.make_assertions(user)

    def test_confirm_registration_with_wrong_security_token_fails(self, api_client):
        user = UserFactory(is_active=False)
        wrong_token = uuid4()

        payload = {"user_id": user.id, "security_token": wrong_token}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == UserDoesNotExist.default_detail
        self.make_assertions(user)

    def test_confirm_registration_with_expired_security_token_fails(self, api_client, mocker):
        user = UserFactory(is_active=False, security_token_expiration_time=now())
        mock = mocker.patch("users.tasks.delete_unregistered_user_after_security_token_expired.delay")

        payload = {"user_id": user.id, "security_token": user.security_token}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == RegistrationTimePassed.default_detail
        mock.assert_called_once_with(str(user.id))
        self.make_assertions(user)
