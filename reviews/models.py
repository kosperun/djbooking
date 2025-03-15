from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from properties.models import Property
from shared.base_model import BaseModel

User = get_user_model()


class Review(BaseModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews")
    text = models.TextField()
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])

    def __str__(self):
        return f"Review for {self.property} with a score {self.score}"
