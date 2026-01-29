from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Category, JobType, Location
from .serializers import JobSerializer, CategorySerializer, JobTypeSerializer, LocationSerializer
from .permissions import IsAdminOrEmployer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from drf_spectacular.utils import extend_schema


# --- Job Views ---
@extend_schema(
    description="List all jobs or create a new job (Admin/Employer only)."
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

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


class JobTypeListCreateView(generics.ListCreateAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]


class JobTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminOrEmployer()]
        return [IsAuthenticatedOrReadOnly()]
