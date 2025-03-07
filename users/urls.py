from django.urls import path

from users.views import UserSingUpAPIView

app_name = "users"

urlpatterns = [
    path("sign-up/", UserSingUpAPIView.as_view(), name="sign-up"),
]
