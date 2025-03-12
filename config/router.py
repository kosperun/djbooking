from django.urls import include, path
from rest_framework_nested import routers

from properties.views.country import CountryViewSet

router = routers.SimpleRouter()
router.register(r"countries", CountryViewSet, basename="countries")

urlpatterns = [
    path("users/", include("users.urls")),
    path("", include(router.urls)),
]
