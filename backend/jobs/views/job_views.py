from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from jobs.models import Job
from jobs.permissions import IsAdminOrEmployer, IsAdminOrResourceOwner
from jobs.serializers import JobSerializer


@extend_schema(
    tags=["Jobs"],
    description="""
### Jobs

**GET**
- Public
- List all active jobs

**POST**
- Admin or Employer only
- Creates a new job
- `created_by` is set automatically
""",
)
class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.select_related(
        "category",
        "job_type",
        "location",
        "company",
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "job_type",
        "location",
        "is_remote",
        "is_active",
    ]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "salary"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    tags=["Jobs"],
    description="""
### Job Detail

**GET**
- Public

**PUT / PATCH / DELETE**
- Admin: any job
- Employer: only jobs they created
""",
)
class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.select_related(
        "category",
        "job_type",
        "location",
        "company",
    )
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrResourceOwner()]
        return [IsAuthenticatedOrReadOnly()]
