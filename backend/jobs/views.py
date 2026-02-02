from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Category, JobType, Location
from .serializers import JobSerializer, CategorySerializer, JobTypeSerializer, LocationSerializer
from .permissions import IsAdminOrEmployer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from drf_spectacular.utils import extend_schema


# --- Job Views ---
@extend_schema(
    description="""List all jobs (public) or create a new job (Admin/Employer only).
    Filterable by category, job_type, location, is_remote, is_active. Searchable
    by title, description, company. Orderable by created_at, salary."""
)
class JobListCreateView(generics.ListCreateAPIView):
    """
    GET: List all jobs (public).
    POST: Create a new job (Admin or Employer only).
    """
    queryset = Job.objects.select_related("category", "job_type", "location").all()
    serializer_class = JobSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "job_type", "location", "is_remote", "is_active"]
    search_fields = ["title", "description", "company"]
    ordering_fields = ["created_at", "salary"]

    def get_permissions(self):
        """
        Assign permissions per HTTP method.
        """
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    description="Retrieve, update, or delete a specific job by ID. GET is public, PUT/PATCH/DELETE require Admin/Employer permissions."
)
class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve job details (public).
    PUT/PATCH: Update job (Admin/Employer only).
    DELETE: Delete job (Admin/Employer only).
    """
    queryset = Job.objects.select_related("category", "job_type", "location").all()
    serializer_class = JobSerializer
    lookup_field = "id"

    def get_permissions(self):
        """
        Assign permissions per HTTP method.
        """
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


# --- Location Views ---
@extend_schema(
    description="List all locations (public) or create a new location (Admin/Employer only)."
)
class LocationListCreateView(generics.ListCreateAPIView):
    """
    GET: List locations (public)
    POST: Create location (Admin/Employer)
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    description="Retrieve, update, or delete a specific location by ID. GET is public, PUT/PATCH/DELETE require Admin/Employer permissions."
)
class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve location (public)
    PUT/PATCH/DELETE: Admin/Employer only
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


# --- Category Views ---
@extend_schema(
    description="List all categories (public) or create a new category (Admin/Employer only)."
)
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List categories (public)
    POST: Create category (Admin/Employer only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    description="Retrieve, update, or delete a specific category by ID. GET is public, PUT/PATCH/DELETE require Admin/Employer permissions."
)
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve category (public)
    PUT/PATCH/DELETE: Admin/Employer only
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


# --- JobType Views ---
@extend_schema(
    description="List all job types (public) or create a new job type (Admin/Employer only)."
)
class JobTypeListCreateView(generics.ListCreateAPIView):
    """
    GET: List job types (public)
    POST: Create job type (Admin/Employer only)
    """
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


@extend_schema(
    description="Retrieve, update, or delete a specific job type by ID. GET is public, PUT/PATCH/DELETE require Admin/Employer permissions."
)
class JobTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve job type (public)
    PUT/PATCH/DELETE: Admin/Employer only
    """
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]