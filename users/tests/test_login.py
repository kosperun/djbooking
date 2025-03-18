import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from conftest import UserFactory

fake = Faker()


@pytest.mark.django_db
class TestUserLoginAPIView:
    def test_user_login_succeeds(self):
        api_client = APIClient()
        raw_password = fake.password()
        user = UserFactory(password=raw_password)
        url = reverse("login")  # "/api/users/login/"
        payload = {"email": user.email, "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_200_OK
        assert response.data["user_id"] == user.id
        assert response.data["is_user"] is True
        assert response.data["is_partner"] is False

    def test_user_login_with_wrong_email_fails(self):
        api_client = APIClient()
        raw_password = fake.password()
        url = reverse("login")  # "/api/users/login/"
        payload = {"email": fake.email(), "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "No active account found with the given credentials"

    def test_user_login_with_wrong_password_fails(self):
        api_client = APIClient()
        wrong_password = fake.password()
        user = UserFactory()
        url = reverse("login")  # "/api/users/login/"
        payload = {"email": user.email, "password": wrong_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "No active account found with the given credentials"

    def test_inactive_user_login_fails(self):
        api_client = APIClient()
        raw_password = fake.password()
        user = UserFactory(password=raw_password, is_active=False)

        url = reverse("login")  # "/api/users/login/"
        payload = {"email": user.email, "password": raw_password}
        response = api_client.post(url, payload)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "No active account found with the given credentials"
