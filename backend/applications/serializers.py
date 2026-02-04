from accounts.serializers import UserSerializer
from jobs.serializers import JobSerializer
from rest_framework import serializers

from .models import Application


# ============================================================
# CREATE APPLICATION
# ============================================================
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "job", "cover_letter", "resume")

    def validate(self, attrs):
        user = self.context["request"].user
        job = attrs["job"]

        if user.role != user.Role.JOB_SEEKER:
            raise serializers.ValidationError("Only job seekers can apply for jobs.")

        if not job.is_active:
            raise serializers.ValidationError(
                "This job is no longer accepting applications."
            )

        if Application.objects.filter(applicant=user, job=job).exists():
            raise serializers.ValidationError("You have already applied for this job.")

        return attrs

    def create(self, validated_data):
        return Application.objects.create(
            applicant=self.context["request"].user,
            **validated_data,
        )


# ============================================================
# READ APPLICATION (LIST / DETAIL)
# ============================================================
class ApplicationReadSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "applicant",
            "job",
            "cover_letter",
            "resume",
            "status",
            "created_at",
            "updated_at",
            "reviewed_at",
            "withdrawn_at",
        )


# ============================================================
# STATUS UPDATE (EMPLOYER / ADMIN)
# ============================================================
class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("status",)

    def validate_status(self, value):
        if value == Application.Status.WITHDRAWN:
            raise serializers.ValidationError(
                "Employers/Admins cannot withdraw applications."
            )
        return value
