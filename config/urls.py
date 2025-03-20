"""
URL configuration for djbooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from config.router import urlpatterns as api_urlpatterns
from payments.views import StripeWebhooksAPIView
from users.views import BlacklistRefreshView, UserLoginAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/login/", UserLoginAPIView.as_view(), name="login"),
    path("api/logout/", BlacklistRefreshView.as_view(), name="logout"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/payments/webhook/", StripeWebhooksAPIView.as_view(), name="payments"),
    path("api/", include(api_urlpatterns)),
    # Swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
