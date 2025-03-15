from django.contrib.auth import get_user_model
from django.db import models

from shared.base_model import BaseModel

User = get_user_model()


class Country(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class City(BaseModel):
    country = models.ForeignKey(Country, related_name="cities", on_delete=models.CASCADE)
    region = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Property(BaseModel):
    class Type(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        HOME = "home", "Home"
        HOTEL = "hotel", "Hotel"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=Type.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="cities")
    district = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    capacity = models.PositiveSmallIntegerField(default=1)
    number_of_rooms = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return f"{self.name} in {self.city}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


def images_folder(instance, filename):
    return f"{instance.property}/{filename}"


class PropertyImage(BaseModel):
    image = models.ImageField(upload_to=images_folder)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return str(self.id)
