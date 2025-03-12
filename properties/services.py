from uuid import UUID

from properties.models import Country
from shared.permissions import check_staff_permissions
from users.models import User


def country_create(*, actor: User, name: str) -> Country:
    check_staff_permissions(actor)
    country = Country(name=name)
    country.save()
    return country


def country_update(*, actor: User, country_id: UUID, **kwargs) -> Country:
    check_staff_permissions(actor)
    country = Country.objects.get(id=country_id)
    for field, value in kwargs.items():
        setattr(country, field, value)
    country.save()
    return country


def country_delete(*, actor: User, country_id: UUID) -> tuple:
    check_staff_permissions(actor)
    country = Country.objects.get(id=country_id)
    return country.delete()
