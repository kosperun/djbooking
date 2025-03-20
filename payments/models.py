from django.conf import settings
from django.db import models

from shared.base_model import BaseModel


class PaymentUser(BaseModel):
    """Model to separate payment concerns from user data."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_user")
    customer_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.email} {self.customer_id}"

    class Meta:
        verbose_name = "Payment User"
        verbose_name_plural = "Payment Users"
