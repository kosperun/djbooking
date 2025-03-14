from typing import Union
from uuid import UUID

from properties.models import City, Country
from shared.utils import paginate_queryset, sort_queryset


def country_retrieve(*, country_id: UUID) -> Country:
    return Country.objects.get(id=country_id)


def country_get_paginated_list(*, query_params: dict) -> dict[str, Union[int, list[Country]]]:
    countries = Country.objects.all()
    sorted_countries = sort_queryset(countries, query_params)
    return paginate_queryset(sorted_countries, query_params)


def city_retrieve(city_id: UUID) -> City:
    city = City.objects.get(id=city_id)
    return city


def city_get_paginated_list(country_id: UUID, query_params: dict) -> dict[str, Union[int, list[City]]]:
    cities = City.objects.filter(country__id=country_id)
    sorted_cities = sort_queryset(cities, query_params)
    return paginate_queryset(sorted_cities, query_params)
