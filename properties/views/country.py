"""API for management of countries."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from properties.selectors import country_get_paginated_list, country_retrieve
from properties.serializers import (
    CountryCreateInputSerializer,
    CountryOutputSerializer,
    CountryPaginatedOutputSerializer,
    CountryUpdateInputSerializer,
)
from properties.services import country_create, country_delete, country_update
from shared.permissions import IsStaffUser


class CountryViewSet(ViewSet):
    """ViewSet for countries API."""

    permission_classes = (IsAdminUser, IsStaffUser)

    @extend_schema(
        request=CountryCreateInputSerializer,
        responses={
            201: CountryOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Allow admin to add a country",
    )
    def create(self, request):
        """Create a country."""
        incoming_data = CountryCreateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        country = country_create(**incoming_data.validated_data)
        output_serializer = CountryOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=None,
        responses={
            200: CountryOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Allow admin to retrieve a country",
    )
    def retrieve(self, request, pk):
        """Get a country's details."""
        country = country_retrieve(country_id=pk)
        output_serializer = CountryOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            200: CountryPaginatedOutputSerializer,
        },
        summary="List all available countries by admin",
    )
    def list(self, request):
        """List all countries."""
        countries = country_get_paginated_list(query_params=request.query_params)
        output_serializer = CountryPaginatedOutputSerializer(countries)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=CountryUpdateInputSerializer,
        responses={
            200: CountryOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Edit country's details by admin",
    )
    def update(self, request, pk):
        """Update a country's details."""
        incoming_data = CountryUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        country = country_update(country_id=pk, **incoming_data.validated_data)
        output_serializer = CountryOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete a country by admin",
    )
    def destroy(self, request, pk):
        """Delete a country."""
        country_delete(country_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
