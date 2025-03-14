from decimal import Decimal
from typing import Optional
from uuid import UUID

from properties.models import City, Country, Property
from properties.selectors import city_retrieve, property_annotate_with_average_ratings
from users.models import User


def country_create(name: str) -> Country:
    country = Country(name=name)
    country.save()
    return country


def country_update(country_id: UUID, **kwargs) -> Country:
    country = Country.objects.get(id=country_id)
    for field, value in kwargs.items():
        setattr(country, field, value)
    country.save()
    return country


def country_delete(country_id: UUID) -> tuple:
    country = Country.objects.get(id=country_id)
    return country.delete()


def city_create(country_id: UUID, name: str, region: str = "") -> City:
    country = Country.objects.get(id=country_id)
    city = City(country=country, name=name, region=region)
    city.save()
    return city


def city_update(city_id: UUID, **kwargs) -> City:
    city = City.objects.get(id=city_id)
    for field, value in kwargs.items():
        setattr(city, field, value)
    city.save()
    return city


def city_delete(city_id: UUID) -> tuple:
    city = City.objects.get(id=city_id)
    return city.delete()


def property_create(
    owner: User,
    name: str,
    type: str,
    city_id: UUID,
    street: str,
    house_number: str,
    zip_code: str,
    price: Decimal,
    email: Optional[str] = "",
    phone_number: Optional[str] = "",
    district: Optional[str] = "",
) -> Property:
    city = city_retrieve(city_id)
    new_property = Property(
        name=name,
        type=type,
        owner=owner,
        city=city,
        district=district,
        street=street,
        house_number=house_number,
        zip_code=zip_code,
        phone_number=phone_number,
        email=email,
        price=price,
    )
    new_property.save()
    return new_property


def property_update(property_obj: Property, **kwargs) -> Property:
    for field, value in kwargs.items():
        setattr(property_obj, field, value)
    property_obj.save()
    return property_obj


def property_delete(property_obj: Property) -> tuple:
    return property_obj.delete()


def property_retrieve_with_average_rating(property_id: UUID) -> Optional[Property]:
    property_obj = Property.objects.filter(id=property_id)
    return property_annotate_with_average_ratings(property_obj).first()
