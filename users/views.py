from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from users.exceptions import MissingTokenOrEmail
from users.selectors import get_user_by_security_token_and_email
from users.services import user_create


class UserSingUpAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        email = serializers.EmailField()

    @extend_schema(
        request=InputSerializer,
        responses={
            201: OutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Sign up",
    )
    def post(self, request):
        """
        is_user = "Do you plan to rent listed properties?"\n
        is_partner = "Do you plan to list property for rent?"
        """
        incoming_data = self.InputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = user_create(**incoming_data.validated_data, is_active=False)
        output_serializer = self.OutputSerializer(user)
        return Response(output_serializer.data, status=HTTP_201_CREATED)


class UserGetByTokenAndEmailAPIView(APIView):
    """
    API to check if a user with such security token and email exists.

    This is an intermediate API just for FE side verifications before registration-confirm,
    password-forget-reset or email-change flows.

    If a token/email is wrong - just display an error to a user and no need to collect their
    password/email to change.

    If a user exists - proceed further to confirm registration or collect
    their email/password to change.
    """

    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter("token", type=OpenApiTypes.UUID, location=OpenApiParameter.QUERY),
            OpenApiParameter("email", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses={
            200: inline_serializer(
                name="retrieve_user_id",
                fields={"user_id": serializers.UUIDField()},
            ),
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get user by security token and email",
    )
    def get(self, request):
        token = request.query_params.get("token")
        email = request.query_params.get("email")
        if not (token and email):
            raise MissingTokenOrEmail()
        user = get_user_by_security_token_and_email(token, email)
        return Response({"user_id": user.id}, status=HTTP_200_OK)
