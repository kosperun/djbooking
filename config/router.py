from django.urls import include, path
from rest_framework_nested import routers

router = routers.SimpleRouter()

urlpatterns = [
    path("users/", include("users.urls")),
    path("", include(router.urls)),
]
