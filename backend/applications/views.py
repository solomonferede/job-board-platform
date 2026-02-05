from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .permissions import IsAdmin, IsApplicantOwner, IsJobOwner, IsJobSeeker
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationReadSerializer,
    ApplicationStatusUpdateSerializer,
)


@extend_schema(
    tags=["Applications"],
    summary="List Applications for a Job or Apply to a Job",
    description="""
This endpoint is nested under a specific job: `/api/v1/jobs/{job_pk}/applications/`.

### GET
- **Purpose:** Retrieve all applications submitted for the specified job.
- **Access:** Job Owner (employer who created the job) or Admin.
- **Response:** List of application objects including applicant details, status, cover letter, resume, and timestamps.

### POST
- **Purpose:** Submit a new application for the specified job.
- **Access:** Authenticated Job Seeker only.
- **Behavior:** Automatically assigns the authenticated user as the applicant and associates the application with the specified job.
- **Validation:** Prevents duplicate applications from the same user for the same job.
- **Response:** Newly created application object.
""",
)
class JobApplicationListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Application.objects.filter(job_id=self.kwargs.get("job_pk"))

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ApplicationCreateSerializer
        return ApplicationReadSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, IsJobSeeker]
        else:
            self.permission_classes = [IsAuthenticated, IsJobOwner | IsAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user, job_id=self.kwargs.get("job_pk"))


@extend_schema(
    tags=["Applications"],
    summary="List My Applications",
    description="""
### GET /api/v1/applications/my/

- **Purpose:** Retrieve all applications submitted by the currently authenticated user (Job Seeker).
- **Access:** Job Seeker only.
- **Response:** List of application objects with details such as job, company, status, cover letter, resume, and timestamps.
- **Behavior:** Sorted by creation date descending (most recent first).
""",
)
class MyApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationReadSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)


@extend_schema(
    tags=["Applications"],
    summary="Retrieve, Update Status of, or Withdraw an Application",
    description="""
### GET / PATCH / DELETE /api/v1/applications/{application_id}/

**GET**
- **Purpose:** Retrieve full details of a specific application.
- **Access:** 
  - Applicant (owner of the application)
  - Job Owner (employer of the job)
  - Admin
- **Response:** Single application object with all relevant fields.

**PATCH**
- **Purpose:** Update the status of an application (e.g., 'REVIEWED', 'SHORTLISTED', 'ACCEPTED', 'REJECTED').
- **Access:** Job Owner or Admin.
- **Behavior:** Sets `reviewed_at` timestamp automatically.

**DELETE**
- **Purpose:** Withdraw an application (soft delete).
- **Access:** Applicant only.
- **Behavior:** Marks the application status as `WITHDRAWN` instead of deleting the record.
- **Response:** Updated application object with `WITHDRAWN` status.
""",
)
class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ApplicationStatusUpdateSerializer
        return ApplicationReadSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated, IsApplicantOwner]
        elif self.request.method == "PATCH":
            self.permission_classes = [IsAuthenticated, IsJobOwner | IsAdmin]
        else:  # GET
            self.permission_classes = [
                IsAuthenticated,
                IsApplicantOwner | IsJobOwner | IsAdmin,
            ]
        return super().get_permissions()

    def perform_destroy(self, instance):
        # Instead of deleting, we mark as withdrawn
        instance.status = Application.Status.WITHDRAWN
        instance.save()
