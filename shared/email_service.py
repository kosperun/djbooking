from abc import ABC, abstractmethod

from django.conf import settings
from django.utils.module_loading import import_string


class BaseEmailService(ABC):
    """Abstract Base EmailService class"""

    def __init__(self):
        super().__init__()
        self.from_email = settings.DEFAULT_FROM_EMAIL

    @abstractmethod
    def send_confirmation_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_change_password_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_forgot_password_email(self, *, email: str, username: str, link: str):
        pass

    @abstractmethod
    def send_change_email_link(self, *, email: str, link: str):
        pass

    @abstractmethod
    def send_booking_confirmation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        pass

    @abstractmethod
    def send_booking_confirmation_email_to_owner(
        self,
        *,
        email: str,
        owner_name: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        pass

    @abstractmethod
    def send_booking_cancellation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
    ):
        pass

    @abstractmethod
    def send_booking_cancellation_email_to_owner(
        self,
        *,
        email: str,
        owner_name: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        pass


class DummyEmailService(BaseEmailService):
    """Dummy EmailService class"""

    def __init__(self):
        super().__init__()

    def send_confirmation_link(self, *, email: str, link: str):
        print("Confirmation Link Sent!")

    def send_change_password_link(self, *, email: str, link: str):
        print("Password Link Sent!")

    def send_forgot_password_email(self, *, email: str, username: str, link: str):
        print("Email to reset password sent!")

    def send_change_email_link(self, *, email: str, link: str):
        print("Email to reset email sent!")

    def send_booking_confirmation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        print("Booking confirmation sent!")

    def send_booking_confirmation_email_to_owner(
        self,
        *,
        email: str,
        owner_name: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        print("Booking confirmation sent!")

    def send_booking_cancellation_email_to_user(
        self,
        *,
        email: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
    ):
        print("Booking cancellation sent!")

    def send_booking_cancellation_email_to_owner(
        self,
        *,
        email: str,
        owner_name: str,
        username: str,
        lodging_name: str,
        city: str,
        date_from: str,
        date_to: str,
        reference_code: str,
    ):
        print("Booking cancellation sent!")


EmailService = import_string(settings.EMAIL_SERVICE)()
