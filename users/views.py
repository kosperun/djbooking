from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

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
