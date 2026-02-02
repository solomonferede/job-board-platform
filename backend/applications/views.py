from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationReadSerializer,
    ApplicationStatusUpdateSerializer,
)
from .permissions import IsJobSeeker, IsEmployerOwner, IsAdmin
from .services import withdraw_application, update_application_status

from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Applications"],
    description="Apply for a job. Authenticated job seekers can submit applications for active job postings."
)
class ApplyJobView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]


@extend_schema(
    tags=["Applications"],
    description="List all applications submitted by the authenticated job seeker."
)
class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)


@extend_schema(
    tags=["Applications"],
    description="Withdraw an existing application. Only the original applicant can withdraw their application."
)
class WithdrawApplicationView(generics.UpdateAPIView):
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]
    queryset = Application.objects.all()

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        if application.applicant != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            withdraw_application(application)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        return Response(ApplicationReadSerializer(application).data)


@extend_schema(
    tags=["Applications"],
    description="List all applications for a specific job. Only the job's employer can view these applications."
)
class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwner]

    def get_queryset(self):
        return Application.objects.filter(
            job_id=self.kwargs["job_id"],
            job__employer=self.request.user,
        )


@extend_schema(
    tags=["Applications"],
    description="Update the status of an application (e.g., pending, accepted, rejected). Available to job employers and admins."
)
class UpdateApplicationStatusView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwner | IsAdmin]
    queryset = Application.objects.all()

    def perform_update(self, serializer):
        update_application_status(
            self.get_object(),
            serializer.validated_data["status"],
        )


@extend_schema(
    tags=["Applications"],
    description="List all applications in the system. Admin-only endpoint for comprehensive application management."
)
class AdminAllApplicationsView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsAdmin]