from typing import Union
from uuid import UUID

from reviews.models import Review
from shared.utils import paginate_queryset, sort_queryset
from users.models import User


def review_retrieve(review_id: UUID) -> Review:
    return Review.objects.get(id=review_id)


def review_get_paginated_list_by_property(property_id: UUID, query_params: dict) -> dict[str, Union[int, list[Review]]]:
    reviews = Review.objects.filter(property__id=property_id)
    sorted_reviews = sort_queryset(reviews, query_params)
    return paginate_queryset(sorted_reviews, query_params)


def review_get_paginated_list_by_user(user: User, query_params: dict) -> dict[str, Union[int, list[Review]]]:
    my_reviews = Review.objects.filter(user=user)
    my_sorted_reviews = sort_queryset(my_reviews, query_params)
    return paginate_queryset(my_sorted_reviews, query_params)
