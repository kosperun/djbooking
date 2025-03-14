from uuid import UUID

from properties.models import City, Country


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
