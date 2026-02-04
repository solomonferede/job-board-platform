from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category, Company, Job, JobType, Location
from .permissions import IsAdminOrEmployer, IsAdminOrResourceOwner
from .serializers import (
    CategorySerializer,
    CompanySerializer,
    JobSerializer,
    JobTypeSerializer,
    LocationSerializer,
)

# ============================================================
# JOB VIEWS
# ============================================================


@extend_schema(
    tags=["Jobs"],
    description="""
### Job Listings & Creation

**Public users**
- Can list and view jobs.

**Authenticated Admins & Employers**
- Can create job postings.

---

### 🔍 Filtering
You can filter jobs by:
- `category`
- `job_type`
- `location`
- `is_remote`
- `is_active`

### 🔎 Search
Search by:
- `title`
- `description`
- `company`

### ↕ Ordering
Order results by:
- `created_at`
- `salary`

---

### 🔐 Permissions
- **GET** → Public
- **POST** → Admin / Employer only
""",
)
class JobListCreateView(generics.ListCreateAPIView):
    """
    GET: List all jobs (public).
    POST: Create a new job (Admin or Employer only).
    """

    queryset = Job.objects.select_related(
        "category", "job_type", "location", "company"
    ).all()
    serializer_class = JobSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "job_type", "location", "is_remote", "is_active"]
    search_fields = ["title", "description", "company"]

    ordering_fields = ["created_at", "salary"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    tags=["Jobs"],
    description="""
### 📄 Job Detail Management

Retrieve, update, or delete a specific job posting.

---

### 🔐 Permissions
- **GET** → Public
- **PUT / PATCH / DELETE**
  - Admin
  - Employer (only jobs they created)

---

### ⚠ Notes
- Employers **cannot modify jobs created by others**
- Admins can manage all jobs
""",
)
class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve job details (public).
    PUT/PATCH/DELETE: Update their own job(Employer only).
    Admins can manage all jobs.
    """

    queryset = Job.objects.select_related("category", "job_type", "location").all()
    serializer_class = JobSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrResourceOwner()]
        return [IsAuthenticatedOrReadOnly()]


# ============================================================
# LOCATION VIEWS
# ============================================================


@extend_schema(
    tags=["Locations"],
    description="""
### 🌍 Job Locations

Manage job locations used for job postings.

---

### 🔐 Permissions
- **GET** → Public
- **POST** → Admin / Employer only
""",
)
class LocationListCreateView(generics.ListCreateAPIView):
    """
    GET: List all locations (public).
    POST: Create a new location (Admin/Employer only).
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    tags=["Locations"],
    description="""
### 📍 Location Detail Management

Retrieve, update, or delete a specific location.

---

### 🔐 Permissions
- **GET** → Public
- **PUT / PATCH / DELETE** → Admin / Employer only
""",
)
class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve location (public).
    PUT/PATCH/DELETE: Admin/Employer only.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


# ============================================================
# CATEGORY VIEWS
# ============================================================


@extend_schema(
    tags=["Job Categories"],
    description="""
### 🗂 Job Categories

Categories represent industries or job domains
(e.g., IT, Healthcare, Marketing).

---

### 🔐 Permissions
- **GET** → Public
- **POST** → Admin / Employer only
""",
)
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List all job categories (public).
    POST: Create category (Admin/Employer only).
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    tags=["Job Categories"],
    description="""
### 🗂 Category Detail Management

Retrieve, update, or delete a job category.

---

### 🔐 Permissions
- **GET** → Public
- **PUT / PATCH / DELETE** → Admin / Employer only
""",
)
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve category (public).
    PUT/PATCH/DELETE: Admin/Employer only.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


# ============================================================
# JOB TYPE VIEWS
# ============================================================


@extend_schema(
    tags=["Job Types"],
    description="""
### 🧾 Job Types

Defines employment type:
- Full-time
- Part-time
- Contract
- Internship

---

### 🔐 Permissions
- **GET** → Public
- **POST** → Admin / Employer only
""",
)
class JobTypeListCreateView(generics.ListCreateAPIView):
    """
    GET: List job types (public).
    POST: Create job type (Admin/Employer only).
    """

    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    tags=["Job Types"],
    description="""
### 🧾 Job Type Detail Management

Retrieve, update, or delete a job type.

---

### 🔐 Permissions
- **GET** → Public
- **PUT / PATCH / DELETE** → Admin / Employer only
""",
)
class JobTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve job type (public).
    PUT/PATCH/DELETE: Admin/Employer only.
    """

    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


# ============================================================
# COMPANY VIEWS
# ============================================================


@extend_schema(
    tags=["Companies"],
    description="""
### 🏢 Company Listings & Creation

**Public users**
- Can list and view companies.

**Authenticated Admins**
- Can create new companies.

---

### 🔐 Permissions
- **GET** → Public
- **POST** → Admin only
""",
)
class CompanyListCreateView(generics.ListCreateAPIView):
    """
    GET: List all companies (public).
    POST: Create a new company (Admin only).
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            # Only admins can create
            return [IsAdminOrResourceOwner()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    tags=["Companies"],
    description="""
### 🏢 Company Detail Management

Retrieve, update, or delete a specific company by ID.

---

### 🔐 Permissions
- **GET** → Public
- **PUT / PATCH / DELETE** → Admin only

---
""",
)
class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve company details (public).
    PUT/PATCH/DELETE: Admin only.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            # Only admins can update or delete companies
            return [IsAdminOrResourceOwner()]
        return [IsAuthenticatedOrReadOnly()]
