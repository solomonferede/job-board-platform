from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from jobs.serializers import CompanySerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for authenticated users.
    """

    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "company",
        )
        read_only_fields = ("role", "company")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Public registration serializer.
    Always creates a JOB_SEEKER.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )
        read_only_fields = ("role", "company")

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=User.Role.JOB_SEEKER,
        )
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Allows limited profile updates.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Admin-level serializer.
    Allows role & status management.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "company",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("date_joined", "last_login")

    def validate_password(self, value):
        validate_password(value)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Password change serializer.
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        try:
            validate_password(value, self.context["request"].user)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
