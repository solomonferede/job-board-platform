from drf_spectacular.utils import extend_schema
from rest_framework import generics

from jobs.models import Category
from jobs.permissions import IsAdminOrReadOnly
from jobs.serializers import CategorySerializer


@extend_schema(
    tags=["Categories"],
    summary="List or Create Job Categories",
    description="""
    - **List:** Returns a list of all available job categories.
    - **Create:** Creates a new job category. (Admin only)
    """,
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    tags=["Categories"],
    summary="Retrieve, Update, or Delete a Job Category",
    description="""
    - **Retrieve:** Returns the details of a specific job category.
    - **Update:** Modifies a job category. (Admin only)
    - **Delete:** Removes a job category. (Admin only)
    """,
)
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "id"
