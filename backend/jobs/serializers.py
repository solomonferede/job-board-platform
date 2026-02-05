from rest_framework import serializers

from .models import Category, Company, Job, JobType, Location


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("created_by",)


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    job_type = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
