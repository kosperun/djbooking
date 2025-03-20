from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from conftest import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestEmailChangeRequestAPIView:
    url = reverse("users:request-change-email")

    def test_request_email_change_succeeds(self, authenticated_client, mocker):
        user = UserFactory()
        old_email = user.email
        new_email = fake.email()

        mock_task = mocker.patch("users.tasks.send_change_email_link_task.delay", return_value=None)
        payload = {"new_email": new_email}
        client = authenticated_client(user)
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_202_ACCEPTED
        user.refresh_from_db()
        # Assert that the email has not been changed yet - only after the request is confirmed
        assert user.email == old_email
        mock_task.assert_called_once_with(new_email, str(user.security_token))

    def test_request_email_change_without_new_email_fails(self, authenticated_client):
        user = UserFactory()
        old_email = user.email

        payload = {}
        client = authenticated_client(user)
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["new_email"][0] == "This field is required."
        user.refresh_from_db()
        assert user.email == old_email

    def test_request_email_change_with_invalid_email_fails(self, authenticated_client):
        user = UserFactory()
        old_email = user.email

        payload = {"new_email": "email @1.com"}
        client = authenticated_client(user)
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["new_email"][0] == "Enter a valid email address."
        user.refresh_from_db()
        assert user.email == old_email

    def test_request_email_change_by_logged_out_user_fails(self):
        old_email = fake.email()
        new_email = fake.email()
        user = UserFactory(email=old_email)

        payload = {"new_email": new_email}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert str(response.data["detail"]) == "Authentication credentials were not provided."
        user.refresh_from_db()
        assert user.email == old_email


@pytest.mark.django_db
class TestEmailChangeConfirmAPIView:
    url = reverse("users:confirm-change-email")

    def setup_user(self, old_email=fake.email(), user_security_token=uuid4()):
        user = UserFactory(email=old_email, security_token=user_security_token)
        return user

    def test_email_change_succeeds(self):
        user = self.setup_user()
        new_email = fake.email()
        security_token = user.security_token

        payload = {"security_token": security_token, "new_email": new_email}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_200_OK
        user.refresh_from_db()
        assert user.email == new_email
        assert user.security_token == ""

    def test_email_change_with_wrong_token_fails(self):
        user = self.setup_user()
        old_email = user.email
        new_email = fake.email()

        wrong_security_token = uuid4()

        payload = {"security_token": wrong_security_token, "new_email": new_email}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_404_NOT_FOUND

        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_without_token_fails(self):
        user = self.setup_user()
        old_email = user.email
        new_email = fake.email()

        payload = {"new_email": new_email}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["security_token"][0] == "This field is required."
        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_without_email_fails(self):
        user = self.setup_user()
        old_email = user.email

        payload = {"security_token": user.security_token}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["new_email"][0] == "This field is required."
        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_without_token_and_without_email_fails(self):
        user = self.setup_user()
        old_email = user.email

        payload = {}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["security_token"][0] == "This field is required."
        assert response.data["new_email"][0] == "This field is required."
        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""

    def test_email_change_with_invalid_email_fails(self):
        user = self.setup_user()
        old_email = user.email

        payload = {"security_token": user.security_token, "new_email": "new_email@com"}
        client = APIClient()
        response = client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data["new_email"][0] == "Enter a valid email address."
        user.refresh_from_db()
        assert user.email == old_email
        assert user.security_token != ""
