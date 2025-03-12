from typing import Union
from uuid import UUID

from properties.models import City, Country
from shared.permissions import check_staff_permissions
from shared.utils import paginate_queryset, sort_queryset
from users.models import User


def country_retrieve(*, actor: User, country_id: UUID) -> Country:
    check_staff_permissions(actor)
    return Country.objects.get(id=country_id)


def country_get_paginated_list(*, actor: User, query_params: dict) -> dict[str, Union[int, list[Country]]]:
    check_staff_permissions(actor)
    countries = Country.objects.all()
    sorted_countries = sort_queryset(countries, query_params)
    return paginate_queryset(sorted_countries, query_params)


def city_retrieve(actor: User, city_id: UUID) -> City:
    check_staff_permissions(actor)
    city = City.objects.get(id=city_id)
    return city


def city_get_paginated_list(actor: User, country_id: UUID, query_params: dict) -> dict[str, Union[int, list[City]]]:
    check_staff_permissions(actor)
    cities = City.objects.filter(country__id=country_id)
    sorted_cities = sort_queryset(cities, query_params)
    return paginate_queryset(sorted_cities, query_params)
