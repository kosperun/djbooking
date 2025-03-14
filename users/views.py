from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_205_RESET_CONTENT
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from users.exceptions import MissingTokenOrEmail
from users.selectors import get_user_by_security_token_and_email
from users.serializers import (
    EmailChangeConfirmInputSerializer,
    EmailChangeRequestInputSerializer,
    PasswordChangeInputSerializer,
    PasswordResetConfirmInputSerializer,
    SendForgotPasswordLinkInputSerializer,
    UserLoginOutputSerializer,
    UserRegistrationConfirmInputSerializer,
    UserRetrieveUpdateInputSerializer,
    UserRetrieveUpdateOutputSerializer,
    UserSingUpInputSerializer,
    UserSingUpOutputSerializer,
)
from users.services import (
    change_email,
    change_password,
    confirm_registration,
    confirm_reset_password,
    send_change_email_link,
    send_forgot_password_link,
    update_user,
    user_create,
)


class UserSingUpAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=UserSingUpInputSerializer,
        responses={
            201: UserSingUpOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Sign up",
    )
    def post(self, request):
        """
        is_user = "Do you plan to rent listed properties?"\n
        is_partner = "Do you plan to list property for rent?"
        """
        incoming_data = UserSingUpInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = user_create(**incoming_data.validated_data, is_active=False)
        output_serializer = UserSingUpOutputSerializer(user)
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


class UserRegistrationConfirmAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=UserRegistrationConfirmInputSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Confirm registration",
    )
    def post(self, request):
        incoming_data = UserRegistrationConfirmInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        confirm_registration(**incoming_data.validated_data)
        return Response(status=HTTP_200_OK)


class UserLoginAPIView(TokenViewBase):
    serializer_class = UserLoginOutputSerializer


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()
        return Response(status=HTTP_205_RESET_CONTENT)


class PasswordChangeAPIView(APIView):
    @extend_schema(
        request=PasswordChangeInputSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Change password",
    )
    def patch(self, request):
        input_serializer = PasswordChangeInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        change_password(user=request.user, **input_serializer.validated_data)
        return Response(status=HTTP_200_OK)


class SendForgotPasswordLinkAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        request=SendForgotPasswordLinkInputSerializer,
        responses={
            202: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Send forgot password link",
    )
    def post(self, request):
        incoming_data = SendForgotPasswordLinkInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        send_forgot_password_link(**incoming_data.validated_data)
        return Response(status=HTTP_202_ACCEPTED)


class PasswordResetConfirmAPIView(APIView):
    """
    This is the second step of 'forgot password' flow.
    This API should be used after SendForgotPasswordLinkAPIView where a token is sent
    to an email specified by user.

    After a user resets their password via this API they should be logged in via UserLoginAPI.
    """

    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        request=PasswordResetConfirmInputSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Confirm resetting password after forgetting",
    )
    def post(self, request):
        incoming_data = PasswordResetConfirmInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        confirm_reset_password(**incoming_data.validated_data)
        return Response(status=HTTP_200_OK)


class EmailChangeRequestAPIView(APIView):
    @extend_schema(
        request=EmailChangeRequestInputSerializer,
        responses={202: None},
        summary="Send a link to new email",
    )
    def post(self, request):
        input_serializer = EmailChangeRequestInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        send_change_email_link(user=request.user, **input_serializer.validated_data)
        return Response(status=HTTP_202_ACCEPTED)


class EmailChangeConfirmAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        request=EmailChangeConfirmInputSerializer,
        responses={200: None},
        summary="Confirm change email",
    )
    def post(self, request):
        input_serializer = EmailChangeConfirmInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        change_email(**input_serializer.validated_data)
        return Response(status=HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "patch"]  # Remove PUT from RetrieveUpdateAPIView

    @extend_schema(
        request=None,
        responses={
            200: UserRetrieveUpdateOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        methods=["GET"],
        description="Allow a user to retrieve their own profile.",
        summary="Get my details",
    )
    def get(self, request):
        """
        Allow a user to retrieve their own profile.
        """
        output_serializer = UserRetrieveUpdateOutputSerializer(request.user)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=UserRetrieveUpdateInputSerializer,
        responses={
            200: UserRetrieveUpdateOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        methods=["PATCH"],
        description="Allow a user to update their own profile.",
        summary="Update my details",
    )
    def patch(self, request):
        incoming_data = UserRetrieveUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = update_user(user=request.user, **incoming_data.validated_data)
        output_serializer = UserRetrieveUpdateOutputSerializer(user)
        return Response(output_serializer.data, status=HTTP_200_OK)
