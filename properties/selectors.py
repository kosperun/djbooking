from datetime import date
from typing import TYPE_CHECKING, Any, Optional, Union
from uuid import UUID

from django.db.models import Avg, Case, Q, QuerySet, Value, When
from django.db.models.functions import Round

from properties.models import City, Country, Property, Review
from shared.utils import paginate_queryset, sort_queryset

if TYPE_CHECKING:
    from django.db.models.query import ValuesQuerySet


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


def property_retrieve(property_id: UUID) -> Property:
    return Property.objects.get(id=property_id)


def property_get_filtered_list(query_params: dict) -> QuerySet[Property]:
    date_from: date = query_params["date_from"]
    date_to: date = query_params["date_to"]
    capacity = int(query_params.get("capacity", 1))
    number_of_rooms = int(query_params.get("number_of_rooms", 1))
    type = query_params.get("type", "")
    available_only = query_params.get("available_only", False)
    country = query_params.get("country")
    city = query_params.get("city")

    property_filter = _construct_property_filter(capacity, number_of_rooms, type, country, city)
    filtered_properties_ids_list = _get_list_of_filtered_properties_ids(property_filter)
    query_expression = _generate_query_expression_for_filter(date_from, date_to, filtered_properties_ids_list)
    if available_only:
        filtered_properties = _property_filter_by_expression(query_expression)
    else:
        filtered_properties = _get_available_and_unavailable_filtered_properties(query_expression)
    # Add average_rating to each Property
    result = property_annotate_with_average_ratings(filtered_properties).distinct()
    return result


def _construct_property_filter(
    capacity: int, number_of_rooms: int, type: str, country: Optional[str], city: Optional[str]
) -> Q:
    property_filter = Q(
        capacity__gte=capacity,
        number_of_rooms__exact=number_of_rooms,
    )
    if city and country:
        property_filter &= Q(city__name__exact=city, city__country__name__exact=country)
    elif country:
        property_filter &= Q(city__country__name__exact=country)

    if type:
        property_filter &= Q(type__exact=type)
    return property_filter


def _generate_query_expression_for_filter(
    date_from: date, date_to: date, filtered_properties_ids_list: "ValuesQuerySet[Property, Any]"
) -> Q:
    """Generate complex query expression to include only properties in a given city/country that are:
    EITHER not booked at all for given dates
    OR their bookings' dates 'from' and 'to' do not overlap with given dates.
    """
    query_expression = Q(id__in=filtered_properties_ids_list) & (
        Q(booking__isnull=True) | Q(booking__date_to__lte=date_from) | Q(booking__date_from__gte=date_to)
    )
    return query_expression


def _get_list_of_filtered_properties_ids(property_filter: Q) -> "ValuesQuerySet[Property, Any]":
    filtered_properties = Property.objects.filter(property_filter)
    filtered_properties_ids_list = filtered_properties.values_list("id", flat=True)
    return filtered_properties_ids_list


def _property_filter_by_expression(query_expression: Q) -> QuerySet[Property]:
    # TODO: Filter for Bookings status!
    return Property.objects.filter(query_expression)


def _get_available_and_unavailable_filtered_properties(query_expression: Q) -> QuerySet[Property]:
    filtered_properties = Property.objects.annotate(
        available=Case(When(query_expression, then=Value(True)), default=Value(False))
    )
    return filtered_properties


def property_annotate_with_average_ratings(filtered_properties: QuerySet) -> QuerySet[Property]:
    return filtered_properties.annotate(average_rating=Round(Avg("reviews__score"), precision=1))


def property_get_paginated_filtered_list(query_params: dict) -> dict[str, Union[int, list[Property]]]:
    properties = property_get_filtered_list(query_params)
    sorted_properties = sort_queryset(properties, query_params)
    return paginate_queryset(sorted_properties, query_params)


def review_retrieve(review_id: UUID) -> Review:
    return Review.objects.get(id=review_id)


def review_get_list_by_property(property_id: UUID) -> QuerySet[Review]:
    return Review.objects.filter(property__id=property_id)


def review_get_paginated_list_by_property(property_id: UUID, query_params: dict) -> dict[str, Union[int, list[Review]]]:
    reviews = review_get_list_by_property(property_id)
    sorted_reviews = sort_queryset(reviews, query_params)
    return paginate_queryset(sorted_reviews, query_params)
