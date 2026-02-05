from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from jobs.models import Job
from jobs.permissions import IsAdminOrEmployer, IsAdminOrResourceOwner
from jobs.serializers import JobSerializer


@extend_schema(
    tags=["Jobs"],
    summary="List Jobs or Create a Job",
    description="""
### GET /api/v1/jobs/

- **Purpose:** Retrieve a list of jobs.
- **Access:** Public (authentication not required).
- **Behavior:**
  - Returns active jobs by default.
  - Supports filtering, searching, and ordering.
- **Filtering:**
  - `category`
  - `job_type`
  - `location`
  - `is_remote`
  - `is_active`
- **Search:**
  - `title`
  - `description`
- **Ordering:**
  - `created_at`
  - `salary`
- **Performance:**
  - Uses optimized queries with related objects preloaded.

---

### POST /api/v1/jobs/

- **Purpose:** Create a new job posting.
- **Access:** Admin or Employer only.
- **Behavior:**
  - The authenticated user is automatically set as `created_by`.
  - Employers can only create jobs for companies they manage.
- **Validation:**
  - Ensures required job attributes are provided.
- **Response:**
  - Returns the newly created job object.
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
    summary="Retrieve, Update, or Delete a Job",
    description="""
### GET /api/v1/jobs/{id}/

- **Purpose:** Retrieve full details of a single job.
- **Access:** Public.
- **Response:** Job details including category, job type, location, and company.

---

### PUT / PATCH /api/v1/jobs/{id}/

- **Purpose:** Update an existing job.
- **Access:**
  - **Admin:** Can update any job.
  - **Employer:** Can update only jobs they created.
- **Behavior:**
  - Partial updates supported via PATCH.
  - Automatically enforces ownership rules.

---

### DELETE /api/v1/jobs/{id}/

- **Purpose:** Delete a job posting.
- **Access:**
  - **Admin:** Can delete any job.
  - **Employer:** Can delete only jobs they created.
- **Behavior:**
  - Permanently removes the job from the system.
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
