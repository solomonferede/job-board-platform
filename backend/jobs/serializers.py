from rest_framework import serializers
from .models import Job, Category, JobType, Location


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description")


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ("id", "name", "description")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "city", "state", "country", "postal_code")


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    job_type = JobTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    job_type_id = serializers.PrimaryKeyRelatedField(
        queryset=JobType.objects.all(), source="job_type", write_only=True
    )
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source="location", write_only=True
    )

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "description",
            "company",
            "salary",
            "is_remote",
            "is_active",
            "slug",
            "category",
            "category_id",
            "job_type",
            "job_type_id",
            "location",
            "location_id",
            "created_at",
            "updated_at",
        )
