"""API module for the management of Reviews."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from properties.selectors import review_get_paginated_list_by_property, review_retrieve
from properties.serializers import ReviewOutputSerializer, ReviewPaginatedListOutputSerializer


class ReviewViewSet(ViewSet):
    """ViewSet for the management of Reviews by admin."""

    @extend_schema(
        parameters=[OpenApiParameter("property_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)],
        request=None,
        responses={
            200: ReviewPaginatedListOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List all property's reviews by any user",
    )
    def list(self, request, property_pk):
        """List all reviews for a property."""
        reviews = review_get_paginated_list_by_property(property_id=property_pk, query_params=request.query_params)
        output_serializer = ReviewPaginatedListOutputSerializer(reviews)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("property_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: ReviewOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get a review's details by any user",
    )
    def retrieve(self, request, property_pk, pk):  # pylint:disable=unused-argument
        """Get a review's details."""
        review = review_retrieve(review_id=pk)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)
