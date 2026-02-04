from rest_framework import serializers

from .models import Category, Company, Job, JobType, Location


# -------------------------
# Category Serializer
# -------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description")


# -------------------------
# JobType Serializer
# -------------------------
class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ("id", "name", "description")


# -------------------------
# Location Serializer
# -------------------------
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "city", "state", "country", "postal_code")


# -------------------------
# Company Serializer
# -------------------------
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("created_by", "slug", "created_at")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


# -------------------------
# Job Serializer
# -------------------------
class JobSerializer(serializers.ModelSerializer):
    # Nested representations
    company = CompanySerializer(read_only=True)
    category = serializers.StringRelatedField()  # e.g., "IT", "Marketing"
    job_type = serializers.StringRelatedField()  # e.g., "Full-time"
    location = serializers.StringRelatedField()  # e.g., "Addis Ababa, Ethiopia"

    class Meta:
        model = Job
        exclude = ("created_by",)

    def validate(self, attrs):
        user = self.context["request"].user

        # If user has a company, they cannot assign another company
        if (
            user.company
            and attrs.get("company")
            and attrs.get("company") != user.company
        ):
            raise serializers.ValidationError(
                "You can only post jobs for your own company."
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["company"] = user.company  # Automatically assign user's company
        return super().create(validated_data)
