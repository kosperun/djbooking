from django.urls import path

from users.views import UserGetByTokenAndEmailAPIView, UserRegistrationConfirmAPIView, UserSingUpAPIView

app_name = "users"

urlpatterns = [
    path("sign-up/", UserSingUpAPIView.as_view(), name="sign-up"),
    path("token-email/", UserGetByTokenAndEmailAPIView.as_view(), name="get-user-by-token"),
    path("registration-confirm/", UserRegistrationConfirmAPIView.as_view(), name="registration-confirm"),
]
