from rest_framework import serializers
from .models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "job", "cover_letter", "resume"]

    def validate(self, attrs):
        user = self.context["request"].user

        if user.role != user.Role.JOB_SEEKER:
            raise serializers.ValidationError("Only job seekers can apply.")

        if Application.objects.filter(
            applicant=user, job=attrs["job"]
        ).exists():
            raise serializers.ValidationError(
                "You have already applied to this job."
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        return Application.objects.create(
            applicant=user,
            **validated_data,
        )


class ApplicationReadSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField()
    job = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = "__all__"


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]
