from drf_spectacular.utils import extend_schema
from rest_framework import generics

from jobs.models import JobType
from jobs.permissions import IsAdminOrReadOnly
from jobs.serializers import JobTypeSerializer


@extend_schema(
    tags=["Job Types"],
    summary="List or Create Job Types",
    description="""
    - **List:** Returns a list of all available job types (e.g., Full-time, Part-time).
    - **Create:** Creates a new job type. (Admin only)
    """,
)
class JobTypeListCreateView(generics.ListCreateAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    tags=["Job Types"],
    summary="Retrieve, Update, or Delete a Job Type",
    description="""
    - **Retrieve:** Returns the details of a specific job type.
    - **Update:** Modifies a job type. (Admin only)
    - **Delete:** Removes a job type. (Admin only)
    """,
)
class JobTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "id"
