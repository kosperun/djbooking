import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

fake = Faker()

User = get_user_model()


@pytest.mark.django_db
class TestUserSingUpAPIView:
    url = reverse("users:sign-up")  # "/api/users/sign-up/"

    def test_user_sign_up_succeeds(self, api_client, mocker):
        email = fake.email()
        password = fake.password()
        mock_task = mocker.patch("users.tasks.send_confirmation_link_task.delay", return_value=None)

        payload = {"email": email, "password": password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_201_CREATED

        user = User.objects.first()
        assert user is not None
        assert user.email == email
        assert user.is_active is False
        assert user.is_user is True
        assert user.is_partner is False
        assert user.is_staff is False
        mock_task.assert_called_once_with(user.email, user.security_token)

    def test_sign_up_without_email_fails(self, api_client):
        password = fake.password()

        payload = {"password": password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "This field is required." in response.data["email"]

    def test_sign_up_without_password_fails(self, api_client):
        email = fake.email()

        payload = {"email": email}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "This field is required." in response.data["password"]

    def test_sign_up_with_weak_similar_password_fails(self, api_client):
        email = fake.email()
        password = email[1:-1]

        payload = {"email": email, "password": password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "The password is too similar to the email." in response.data["non_field_errors"]

    @pytest.mark.parametrize(
        "password, error_message",
        [("qwertyuiop", "This password is too common."), ("1234567890", "This password is entirely numeric.")],
    )
    def test_sign_up_with_weak_common_password_fails(self, password, error_message, api_client):
        email = fake.email()

        payload = {"email": email, "password": password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert error_message in response.data["non_field_errors"]

    def test_sign_up_with_invalid_email_fails(self, api_client):
        invalid_email = f"{fake.first_name()}@com"
        password = fake.password()

        payload = {"email": invalid_email, "password": password}
        response = api_client.post(self.url, payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "Enter a valid email address." in response.data["email"]
