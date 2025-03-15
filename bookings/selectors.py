from uuid import UUID

from bookings.filters import BookingFilterSet
from bookings.models import Booking
from shared.filters import Filter
from shared.utils import paginate_queryset, sort_queryset
from users.models import User


def booking_retrieve(booking_id: UUID) -> Booking:
    return Booking.objects.get(id=booking_id)


def booking_get_filtered_paginated_list(query_params: dict) -> dict:
    qs = Booking.objects.all()
    filter_decorator = Filter(BookingFilterSet)
    filtered_qs = filter_decorator.filter(queryset=qs, query_params=query_params)
    sorted_qs = sort_queryset(filtered_qs, query_params)
    return paginate_queryset(sorted_qs, query_params)


def booking_get_paginated_list_by_user(user: User, query_params: dict) -> dict:
    bookings = Booking.objects.filter(user=user)
    sorted_bookings = sort_queryset(bookings, query_params)
    return paginate_queryset(sorted_bookings, query_params)
