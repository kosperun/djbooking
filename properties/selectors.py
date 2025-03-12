from typing import Union
from uuid import UUID

from properties.models import Country
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
