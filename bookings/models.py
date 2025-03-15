from random import choice
from string import ascii_uppercase, digits

from django.contrib.auth import get_user_model
from django.db import models

from properties.models import Property
from shared.base_model import BaseModel

User = get_user_model()


def generate_reference_code(size=6, chars=ascii_uppercase + digits):
    return "".join(choice(chars) for _ in range(size))


class Booking(BaseModel):
    class Status(models.TextChoices):
        PAYMENT_PENDING = "payment_pending", "Payment pending"
        PAID = "paid", "Paid"
        CANCELED = "canceled", "Canceled"

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PAYMENT_PENDING)
    payment_intent_id = models.CharField(max_length=255, blank=True)
    payment_expiration_time = models.DateTimeField(blank=True, null=True)
    reference_code = models.CharField(max_length=6, default=generate_reference_code)

    def __str__(self):
        return (
            f"{self.user.email} | {self.property.name} in {self.property.city} | "
            + f"({self.date_from} - {self.date_to})"
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
