from rest_framework import serializers

from .models import Application


class ApplicationCreateSerializer(serializers.ModelSerializer):
    applicant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    job = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = ["id", "applicant", "job", "cover_letter", "resume"]
        read_only_fields = ["applicant", "job"]

    def validate(self, attrs):
        user = self.context["request"].user
        job = self.context["view"].kwargs.get("job_pk")

        if not user.is_job_seeker():
            raise serializers.ValidationError("Only job seekers can apply.")

        if Application.objects.filter(applicant=user, job_id=job).exists():
            raise serializers.ValidationError("You have already applied to this job.")

        return attrs


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
