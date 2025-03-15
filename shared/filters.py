from typing import Optional

from django.db.models import QuerySet
from django_filters.filterset import FilterSetMetaclass


class Filter:
    def __init__(self, filterset: FilterSetMetaclass) -> None:
        self._filterset_class = filterset

    def filter(self, query_params: dict, queryset: Optional[QuerySet] = None) -> QuerySet:
        fs = self._filterset_class(query_params, queryset=queryset)
        return fs.qs
