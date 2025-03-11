from django.urls import path

from users.views import (
    EmailChangeRequestAPIView,
    PasswordChangeAPIView,
    PasswordResetConfirmAPIView,
    SendForgotPasswordLinkAPIView,
    UserGetByTokenAndEmailAPIView,
    UserLoginAPIView,
    UserRegistrationConfirmAPIView,
    UserSingUpAPIView,
)

app_name = "users"

urlpatterns = [
    path("sign-up/", UserSingUpAPIView.as_view(), name="sign-up"),
    path("token-email/", UserGetByTokenAndEmailAPIView.as_view(), name="get-user-by-token"),
    path("registration-confirm/", UserRegistrationConfirmAPIView.as_view(), name="registration-confirm"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("password-change/", PasswordChangeAPIView.as_view(), name="change-password"),
    path("password-reset-link/", SendForgotPasswordLinkAPIView.as_view(), name="send-reset-password-link"),
    path("password-reset-confirmation/", PasswordResetConfirmAPIView.as_view(), name="confirm-reset-password"),
    path("email-change-request/", EmailChangeRequestAPIView.as_view(), name="request-change-email"),
]
