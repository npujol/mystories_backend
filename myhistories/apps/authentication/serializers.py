from django.contrib.auth import authenticate
from rest_framework import serializers

from ..profiles.serializers import ProfileSerializer
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token", "profile"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    profile = ProfileSerializer(read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        return {
            "email": user.email,
            "username": user.username,
            "token": user.token,
            "profile": user.profile,
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    profile = ProfileSerializer(read_only=True, required=False)

    class Meta:
        model = User
        fields = ("email", "username", "password", "token", "profile")

        read_only_fields = ("token",)

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop("password", None)

        profile_data = validated_data.pop("profile", {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance
