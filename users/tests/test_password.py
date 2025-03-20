from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST

from conftest import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestPasswordChangeAPIView:
    url = reverse("users:change-password")

    def test_password_change_succeeds(self, authenticated_client):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)

        payload = {"old_password": old_password, "new_password": new_password}

        client = authenticated_client(user)
        response = client.patch(self.url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(old_password) is False
        assert user.check_password(new_password) is True

    def test_password_change_with_wrong_old_password_fails(self, authenticated_client):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory()

        payload = {"old_password": old_password, "new_password": new_password}

        client = authenticated_client(user)
        response = client.patch(self.url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Wrong password!"
        user.refresh_from_db()
        assert user.check_password(new_password) is False


@pytest.mark.django_db
class TestSendForgotPasswordLinkAPIView:
    def test_forgot_password_succeeds(self, api_client, mocker):
        user = UserFactory()
        security_token = user.security_token
        mock_task = mocker.patch("users.tasks.send_change_password_link_task.delay", return_value=None)

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

    def setup_user(self):
        old_password = fake.password()
        new_password = fake.password()
        user = UserFactory(password=old_password)
        security_token = user.security_token
        return user, old_password, new_password, security_token

    def make_asserts(self, user, old_password, new_password, security_token):
        user.refresh_from_db()
        assert user.check_password(old_password) is True
        assert user.check_password(new_password) is False
        assert user.security_token == security_token

    def test_reset_password_succeeds(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()
        payload = {"security_token": security_token, "email": user.email, "new_password": new_password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password(old_password) is False
        assert user.check_password(new_password) is True
        assert user.security_token == ""

    def test_reset_password_with_wrong_token_fails(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()
        wrong_security_token = uuid4()

        payload = {"security_token": wrong_security_token, "email": user.email, "new_password": new_password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Such user does not exist"
        self.make_asserts(user, old_password, new_password, security_token)

    def test_reset_password_with_wrong_email_fails(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()
        wrong_email = fake.email()

        payload = {"security_token": security_token, "email": wrong_email, "new_password": new_password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Such user does not exist"
        self.make_asserts(user, old_password, new_password, security_token)

    def test_reset_password_with_wrong_token_and_wrong_email_fails(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()
        wrong_security_token = uuid4()
        wrong_email = fake.email()

        payload = {"security_token": wrong_security_token, "email": wrong_email, "new_password": new_password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Such user does not exist"
        self.make_asserts(user, old_password, new_password, security_token)

    def test_reset_password_without_token_fails(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()

        payload = {"email": user.email, "new_password": new_password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "This field is required." in response.data["security_token"]
        self.make_asserts(user, old_password, new_password, security_token)

    def test_reset_password_without_email_fails(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()

        payload = {"security_token": security_token, "new_password": new_password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "This field is required." in response.data["email"]
        self.make_asserts(user, old_password, new_password, security_token)

    def test_reset_password_without_token_and_without_email_fails(self, api_client):
        user, old_password, new_password, security_token = self.setup_user()

        payload = {"new_password": new_password}
        response = api_client.post(self.url, payload)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "This field is required." in response.data["security_token"]
