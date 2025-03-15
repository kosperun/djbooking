"""API module for the management of Reviews."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from properties.selectors import (
    review_get_paginated_list_by_property,
    review_get_paginated_list_by_user,
    review_retrieve,
    review_retrieve_my,
)
from properties.serializers import (
    MyReviewCreateInputSerializer,
    MyReviewOutputSerializer,
    MyReviewsPaginatedListOutputSerializer,
    MyReviewUpdateInputSerializer,
    ReviewOutputSerializer,
    ReviewPaginatedListOutputSerializer,
)
from properties.services import review_create, review_delete, review_update


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


class MyReviewViewSet(ViewSet):
    """ViewSet for the management of Reviews by their users."""

    def _get_and_check_review(self, request, review_id):
        """Retrieve a review and check if the user has permission."""
        review = review_retrieve_my(review_id=review_id)
        if review.user != request.user:
            raise PermissionDenied()
        return review

    @extend_schema(
        request=MyReviewCreateInputSerializer,
        responses={
            201: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Add a review for property",
    )
    def create(self, request):
        """Create new review for a property."""
        input_serializer = MyReviewCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = review_create(user=request.user, **input_serializer.validated_data)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            200: MyReviewsPaginatedListOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List my reviews for all my booked properties",
    )
    def list(self, request):
        """List all reviews by a logged in user."""
        my_reviews = review_get_paginated_list_by_user(user=request.user, query_params=request.query_params)
        output_serializer = MyReviewsPaginatedListOutputSerializer(my_reviews)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: MyReviewOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get my review's details",
    )
    def retrieve(self, request, pk):
        """Get a user's review's details."""
        review = self._get_and_check_review(request, pk)
        output_serializer = MyReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=MyReviewUpdateInputSerializer,
        responses={
            200: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Edit my review",
    )
    def update(self, request, pk):
        """Update a review by its author."""
        review = self._get_and_check_review(request, pk)
        input_serializer = MyReviewUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = review_update(review, **input_serializer.validated_data)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete my review",
    )
    def destroy(self, request, pk):
        """Delete a review by its author."""
        review = self._get_and_check_review(request, pk)
        review_delete(review)
        return Response(status=HTTP_204_NO_CONTENT)
