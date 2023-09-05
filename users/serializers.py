from rest_framework import serializers
from .models import User, UserVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'phone', 'verified']


class UserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = ['user', 'phone', 'verification_code']


class VerificationRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    verification_code = serializers.CharField(max_length=6)


class VerificationResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Error message")


class VerificationErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Error message")


class VerificationFormResponseSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, help_text="Phone number to which the verification code was sent")
    verification_code = serializers.CharField(max_length=6, help_text="Verification code entered by the user")


class HomePageResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="User ID")
    name = serializers.CharField(help_text="Username")
    phone = serializers.CharField(help_text="Phone number")


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=100)
