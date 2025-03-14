"""API module for the management of Properties."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from properties.exceptions import CountryMissingError, WrongOwnerError
from properties.selectors import property_get_paginated_filtered_list, property_retrieve
from properties.serializers import (
    PropertyCreateInputSerializer,
    PropertyCreateOutputSerializer,
    PropertyListPaginatedOutputSerializer,
    PropertyOutputSerializer,
    PropertyUpdateInputSerializer,
)
from properties.services import property_create, property_delete, property_retrieve_with_average_rating, property_update
from shared.permissions import IsPartnerUser


class PropertyViewSet(ViewSet):
    """ViewSet for the Property management"""

    def get_permissions(self):
        """Set respective roles' permissions for ViewSet actions."""
        if self.action in ["list", "retrieve"]:
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "destroy"]:
            self.permission_classes = (IsPartnerUser,)
        else:
            self.permission_classes = (IsPartnerUser,)
        return super().get_permissions()

    @extend_schema(
        request=PropertyCreateInputSerializer,
        responses={
            201: PropertyCreateOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Add a property by partner",
    )
    def create(self, request):
        """Create a new property."""
        input_serializer = PropertyCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        new_property = property_create(actor=request.user, **input_serializer.validated_data)
        output_serializer = PropertyCreateOutputSerializer(new_property)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        description="Filter by country or city. At least one of the two is required",
        parameters=[
            OpenApiParameter(
                name="country",
                description="Filter by country",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="city",
                description="Filter by city",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=None,
        responses={
            200: PropertyListPaginatedOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List properties in a city available for given dates by any user",
    )
    def list(self, request):
        """List properties according to the query_params."""
        if not request.query_params.get("country"):
            raise CountryMissingError()
        properties = property_get_paginated_filtered_list(query_params=request.query_params)
        output_serializer = PropertyListPaginatedOutputSerializer(properties)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Property id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=None,
        responses={
            200: PropertyOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get property's details by any user",
    )
    def retrieve(self, request, pk):
        """Get a property's details

        Args:
            request (HttRequest): request
            pk (UUID): property's id

        Returns:
            HttpResponse: serialized property's details
        """
        property_obj = property_retrieve_with_average_rating(pk)
        output_serializer = PropertyOutputSerializer(property_obj)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Property id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=PropertyUpdateInputSerializer,
        responses={
            200: PropertyOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Update property's details by its owner",
    )
    def update(self, request, pk):
        """Update a property's details."""
        property_obj = property_retrieve(pk)
        if property_obj.owner != request.user:
            raise WrongOwnerError()

        input_serializer = PropertyUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        updated_property = property_update(property_obj=property_obj, **input_serializer.validated_data)
        output_serializer = PropertyOutputSerializer(updated_property)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Property id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete property by its owner",
    )
    def destroy(self, request, pk):
        """Delete a property."""
        property_obj = property_retrieve(pk)
        if property_obj.owner != request.user:
            raise WrongOwnerError()
        property_delete(property_obj)
        return Response(status=HTTP_204_NO_CONTENT)
