from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .permissions import IsAdmin, IsEmployerOwner, IsJobSeeker
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationReadSerializer,
    ApplicationStatusUpdateSerializer,
)
from .services import update_application_status, withdraw_application


# ============================================================
# APPLY FOR JOB
# ============================================================
@extend_schema(
    tags=["Applications"],
    description="""
### 📝 Apply for a Job

Authenticated **job seekers only** can apply to active jobs.

- Prevents duplicate applications
- Automatically assigns applicant
""",
)
class ApplyJobView(generics.CreateAPIView):
    """
    Apply for a Job
    Authenticated job seekers only can apply to active jobs.
    """

    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]


# ============================================================
# MY APPLICATIONS (JOB SEEKER)
# ============================================================
@extend_schema(
    tags=["Applications"],
    description="""
### 📂 My Applications

List all applications submitted by the authenticated job seeker.
""",
)
class MyApplicationsView(generics.ListAPIView):
    """
    List all applications submitted by the authenticated job seeker.
    """

    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return (
            Application.objects.select_related("job", "job__company")
            .filter(applicant=self.request.user)
            .order_by("-created_at")
        )


# ============================================================
# WITHDRAW APPLICATION (JOB SEEKER)
# ============================================================
@extend_schema(
    tags=["Applications"],
    description="""
### ❌ Withdraw Application

Only the original applicant may withdraw their application.
""",
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


# ============================================================
# APPLICATIONS FOR A JOB (EMPLOYER)
# ============================================================
@extend_schema(
    tags=["Applications"],
    description="""
### 📥 Job Applications

Employers can view applications **only for jobs they created**.
""",
)
class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwner]

    def get_queryset(self):
        return Application.objects.select_related("job", "applicant").filter(
            job_id=self.kwargs["job_id"],
            job__created_by=self.request.user,
        )


# ============================================================
# UPDATE APPLICATION STATUS (EMPLOYER / ADMIN)
# ============================================================
@extend_schema(
    tags=["Applications"],
    description="""
### 🔄 Update Application Status

Allowed for:
- Employer (job owner)
- Admin

Statuses:
- Reviewed
- Shortlisted
- Accepted
- Rejected
""",
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


# ============================================================
# ADMIN – ALL APPLICATIONS
# ============================================================
@extend_schema(
    tags=["Applications"],
    description="""
### 🛠 Admin – All Applications

Admin-only endpoint to list **all applications in the system**.
""",
)
class AdminAllApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return (
            Application.objects.select_related("job", "job__company", "applicant")
            .all()
            .order_by("-created_at")
        )
