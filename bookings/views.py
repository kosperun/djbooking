"""Bookings views (APIs)"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from bookings.selectors import booking_get_filtered_paginated_list, booking_get_paginated_list_by_user, booking_retrieve
from bookings.serializers import (
    BookingCreateInputSerializer,
    BookingListPaginatedOutputSerializer,
    BookingOutputSerializer,
)
from bookings.services import booking_create
from shared.permissions import IsStaffUser


class BookingViewSet(ViewSet):
    """ViewSet for bookings management by admin."""

    permission_classes = (IsAdminUser, IsStaffUser)

    @extend_schema(
        request=None,
        responses={200: BookingListPaginatedOutputSerializer},
        summary="List all bookings by admin (filtered)",
        parameters=[
            OpenApiParameter(
                "user_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description=("Filter by user's id"),
            ),
            OpenApiParameter(
                "date_from",
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description=("Filter by date_from - gte"),
            ),
            OpenApiParameter(
                "date_to",
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description=("Filter by date_to - lte"),
            ),
            OpenApiParameter(
                "status",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by status"),
            ),
            OpenApiParameter(
                "property_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description=("Filter by property_id"),
            ),
            OpenApiParameter(
                "owner_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description=("Filter by owner_id"),
            ),
            OpenApiParameter(
                "kind",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by kind"),
            ),
            OpenApiParameter(
                "country_name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by country_name"),
            ),
            OpenApiParameter(
                "region_name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by region_name"),
            ),
            OpenApiParameter(
                "city_name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by city_name"),
            ),
            OpenApiParameter(
                "city_district",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by city_district"),
            ),
            OpenApiParameter(
                "street",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by street"),
            ),
            OpenApiParameter(
                "zip_code",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by zip_code"),
            ),
            OpenApiParameter(
                "email",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by email"),
            ),
            OpenApiParameter(
                "number_of_people",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description=("Filter by number_of_people"),
            ),
            OpenApiParameter(
                "number_of_rooms",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description=("Filter by number_of_rooms"),
            ),
            OpenApiParameter(
                "price_gte",
                OpenApiTypes.DECIMAL,
                OpenApiParameter.QUERY,
                description=("Filter by price_gte"),
            ),
            OpenApiParameter(
                "price_lte",
                OpenApiTypes.DECIMAL,
                OpenApiParameter.QUERY,
                description=("Filter by price_lte"),
            ),
        ],
    )
    def list(self, request):
        """List all bookings filtered by query_params."""
        bookings = booking_get_filtered_paginated_list(query_params=request.query_params)
        output_serializer = BookingListPaginatedOutputSerializer(bookings)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter(name="id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)],
        request=None,
        responses={
            200: BookingOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Retrieve a booking details by admin",
    )
    def retrieve(self, request, pk):
        """Get a booking's details."""
        booking = booking_retrieve(booking_id=pk)
        output_serializer = BookingOutputSerializer(booking)
        return Response(data=output_serializer.data, status=HTTP_200_OK)


class MyBookingViewSet(ViewSet):
    """ViewSet for user's own bookings management."""

    @extend_schema(
        request=BookingCreateInputSerializer,
        responses={
            201: BookingOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Book a property",
    )
    def create(self, request):
        """Book property by user."""
        input_serializer = BookingCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        booking = booking_create(user=request.user, **input_serializer.validated_data)
        output_serializer = BookingOutputSerializer(booking)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={200: BookingListPaginatedOutputSerializer},
        summary="List my bookings",
    )
    def list(self, request):
        """List my bookings."""
        bookings = booking_get_paginated_list_by_user(user=request.user, query_params=request.query_params)
        output_serializer = BookingListPaginatedOutputSerializer(bookings)
        return Response(data=output_serializer.data, status=HTTP_200_OK)
