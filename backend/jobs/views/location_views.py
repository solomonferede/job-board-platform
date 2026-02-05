from drf_spectacular.utils import extend_schema
from rest_framework import generics

from jobs.models import Location
from jobs.permissions import IsAdminOrReadOnly
from jobs.serializers import LocationSerializer


@extend_schema(
    tags=["Locations"],
    summary="List or Create Locations",
    description="""
    - **List:** Returns a list of all available job locations.
    - **Create:** Creates a new job location. (Admin only)
    """,
)
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    tags=["Locations"],
    summary="Retrieve, Update, or Delete a Location",
    description="""
    - **Retrieve:** Returns the details of a specific job location.
    - **Update:** Modifies a job location. (Admin only)
    - **Delete:** Removes a job location. (Admin only)
    """,
)
class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "id"
