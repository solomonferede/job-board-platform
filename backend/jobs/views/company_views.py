from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from jobs.models import Company
from jobs.permissions import IsAdminOrOwnerOrReadOnly
from jobs.serializers import CompanySerializer
from accounts.permissions import IsEmployer


@extend_schema(
    tags=["Companies"],
    summary="List or Create Companies",
    description="""
    - **List:** Returns a list of all companies. (Authenticated users only)
    - **Create:** Creates a new company profile. (Employer role required)
      - An employer can only create one company.
    """,
)
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsEmployer]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        # Check if the employer already has a company
        if Company.objects.filter(created_by=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "You have already created a company."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    tags=["Companies"],
    summary="Retrieve, Update, or Delete a Company",
    description="""
    - **Retrieve:** Returns the details of a specific company.
    - **Update:** Modifies a company's profile. (Owner or Admin only)
    - **Delete:** Removes a company. (Owner or Admin only)
    """,
)
class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    lookup_field = "id"
