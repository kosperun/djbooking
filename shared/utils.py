from django.conf import settings
from django.db.models import QuerySet


def sort_queryset(queryset: QuerySet, query_params: dict) -> QuerySet:
    """Apply custom sorting to querysets according to 'order_by' parameter specified in query params."""
    ordering_args: str = query_params.get("order_by", "")
    if not ordering_args:
        return queryset
    ordering_args_list = ordering_args.split(",")
    return queryset.order_by(*ordering_args_list)


def paginate_queryset(queryset: QuerySet, query_params: dict) -> dict:
    """Apply custom pagination schema for all 'list' APIs.

    Accepts two query parameters:
        page: A numeric value indicating the page number.
        page_size: A numeric value indicating the page size.

    Returns:
        dict with count (int) and results (list).
    """
    count = queryset.count()
    page_size = int(query_params.get("page_size", settings.REST_FRAMEWORK["DEFAULT_PAGE_SIZE"]))
    page = int(query_params.get("page", 1))
    bottom = (page - 1) * page_size
    top = bottom + page_size
    results = queryset[bottom:top]
    return {"count": count, "results": results}
