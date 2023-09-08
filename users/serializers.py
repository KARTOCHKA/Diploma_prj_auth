from rest_framework import serializers
from users.models import User, UserVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'phone', 'verified']


class UserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

    def create(self, validated_data):
        return UserResponseSerializer(**validated_data)

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        return instance


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = ['user', 'phone', 'verification_code']


class VerificationRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    verification_code = serializers.CharField(max_length=6)


class VerificationResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Error message")

    def create(self, validated_data):
        return VerificationResponseSerializer(**validated_data)

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        return instance


class VerificationErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Error message")

    def create(self, validated_data):
        return VerificationErrorResponseSerializer(**validated_data)

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        return instance


class VerificationFormResponseSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, help_text="Phone number to which the verification code was sent")
    verification_code = serializers.CharField(max_length=6, help_text="Verification code entered by the user")

    def create(self, validated_data):
        return VerificationFormResponseSerializer(**validated_data)

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.verification_code = validated_data.get('verification_code', instance.verification_code)
        return instance


class HomePageResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="User ID")
    name = serializers.CharField(help_text="Username")
    phone = serializers.CharField(help_text="Phone number")

    def create(self, validated_data):
        return HomePageResponseSerializer(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        return instance


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return CreateUserSerializer(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.phone = validated_data.get('phone', instance.phone)
        return instance
