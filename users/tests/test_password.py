from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from conftest import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestPasswordChangeAPIView:
    url = reverse("users:change-password")

    def test_password_change_succeeds(self, authenticate_user):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)

        payload = {"old_password": old_password, "new_password": new_password}

        client = authenticate_user(user)
        response = client.patch(self.url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(old_password) is False
        assert user.check_password(new_password) is True

    def test_password_change_with_wrong_old_password_fails(self, authenticate_user):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory()

        payload = {"old_password": old_password, "new_password": new_password}

        client = authenticate_user(user)
        response = client.patch(self.url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Wrong password!"
        user.refresh_from_db()
        assert user.check_password(new_password) is False


@pytest.mark.django_db
class TestSendForgotPasswordLinkAPIView:
    def test_forgot_password_succeeds(self, mocker):
        api_client = APIClient()
        user = UserFactory()

        security_token = user.security_token
        mock_task = mocker.patch(
            "users.tasks.send_change_password_link_task.delay",
            return_value=None,
        )
        payload = {"email": user.email}

        url = reverse("users:send-reset-password-link")
        response = api_client.post(url, payload)
        assert response.status_code == HTTP_202_ACCEPTED

        user.refresh_from_db()
        assert user.security_token != security_token
        mock_task.assert_called_once_with(user.email, user.security_token)


@pytest.mark.django_db
class TestPasswordResetConfirmAPIView:
    url = reverse("users:confirm-reset-password")

    def test_reset_password_succeeds(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token

        payload = {"security_token": security_token, "email": user.email, "new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(old_password) is False
        assert user.check_password(new_password) is True
        assert user.security_token == ""

    def test_reset_password_with_wrong_token_fails(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        wrong_security_token = uuid4()

        payload = {"security_token": wrong_security_token, "email": user.email, "new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Such user does not exist"

        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_with_wrong_email_fails(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        wrong_email = fake.email()

        payload = {"security_token": security_token, "email": wrong_email, "new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Such user does not exist"

        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_with_wrong_token_and_wrong_email_fails(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        wrong_security_token = uuid4()
        wrong_email = fake.email()

        payload = {"security_token": wrong_security_token, "email": wrong_email, "new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Such user does not exist"

        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_without_token_fails(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        old_security_token = user.security_token

        payload = {"email": user.email, "new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["security_token"][0] == "This field is required."

        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == old_security_token

    def test_reset_password_without_email_fails(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token

        payload = {"security_token": security_token, "new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["email"][0] == "This field is required."

        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_without_token_and_without_email_fails(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        old_security_token = user.security_token

        payload = {"new_password": new_password}
        api_client = APIClient()
        response = api_client.post(self.url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["security_token"][0] == "This field is required."

        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == old_security_token
