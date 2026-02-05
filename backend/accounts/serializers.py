from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from jobs.models import Company # Import Company model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(write_only=True, required=False) # Add company_name field

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "role",
            "company_name", # Add company_name here
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        try:
            validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        # Validate company_name for employer users
        if attrs.get("role") == User.Role.EMPLOYER and not attrs.get("company_name"):
            raise serializers.ValidationError(
                {"company_name": "Company name is required for employer users."}
            )
        return attrs

    def create(self, validated_data):
        company_name = validated_data.pop("company_name", None) # Pop company_name

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=validated_data.get("role", User.Role.JOB_SEEKER),
        )
        if user.role == User.Role.EMPLOYER and company_name:
            company = Company.objects.create(name=company_name, created_by=user)
            user.company = company # Assign the created Company object
            user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("username", "email", "date_joined", "last_login")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New passwords must match."}
            )
        try:
            validate_password(data["new_password"], self.context["request"].user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return data