from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import UserSerializer, RegisterSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Authentication"],
    description="Obtain JWT token pair (access + refresh). Provide username and password to authenticate."
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Authentication"],
    description="Refresh JWT access token. Provide a valid refresh token to get a new access token."
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    description="Register a new user account. Requires username, email, password, and optional first_name/last_name. Password is write-only and will be securely hashed. No authentication required.",
    tags=["Authentication"],
)
class RegisterView(generics.CreateAPIView):
    """
    Create a new user account with username, email, and password.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    description="User profile management. GET returns the authenticated user's profile including id, username, email, first_name, last_name, and role.",
    tags=["User Profile"],
)
class ProfileView(APIView):
    """
    View and manage authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Retrieve the current authenticated user's profile details including role information.",
        responses={200: UserSerializer}
    )
    def get(self, request):
        """
        Retrieve the authenticated user's profile with role information.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)