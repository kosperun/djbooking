from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSingUpInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSingUpOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class UserRegistrationConfirmInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    security_token = serializers.UUIDField()


class UserLoginOutputSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.full_name
        data["user_id"] = self.user.id
        data["is_user"] = self.user.is_user
        data["is_partner"] = self.user.is_partner
        return data


class PasswordChangeInputSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class SendForgotPasswordLinkInputSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmInputSerializer(serializers.Serializer):
    security_token = serializers.UUIDField()
    email = serializers.EmailField()
    new_password = serializers.CharField()


class EmailChangeRequestInputSerializer(serializers.Serializer):
    new_email = serializers.EmailField()


class EmailChangeConfirmInputSerializer(serializers.Serializer):
    security_token = serializers.UUIDField()
    new_email = serializers.EmailField()


class UserRetrieveUpdateInputSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    nationality = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)


class UserRetrieveUpdateOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    date_of_birth = serializers.DateField()
    nationality = serializers.CharField()
    gender = serializers.CharField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_user = serializers.BooleanField()
    is_partner = serializers.BooleanField()
