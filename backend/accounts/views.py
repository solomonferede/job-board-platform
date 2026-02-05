from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .models import User
from .permissions import IsAdmin, IsEmployer
from .serializers import (
    AdminUserSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)

# =========================
# Authentication
# =========================


@extend_schema(
    tags=["Authentication"],
    summary="Obtain JWT Access and Refresh Tokens",
    description=(
        "### 🔓 Access\n"
        "- **Public endpoint** (authenticate using valid **username** and **password**\n\n"
        "### ⏱ Token Lifetime\n"
        "- **Access token**: short-lived (~5 minutes)\n"
        "- **Refresh token**: longer-lived (~24 hours)\n\n"
        "### 📥 Example Request Body\n"
        "```json\n"
        "{\n"
        '  "username": "john_doe",\n'
        '  "password": "securepassword123"\n'
        "}\n"
        "```"
    ),
    responses={
        200: {
            "description": "Authentication successful",
            "content": {
                "application/json": {
                    "example": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    }
                }
            },
        },
        401: {"description": "Invalid username or password"},
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Authentication"],
    summary="Refresh JWT Access Token",
    description=(
        "Refresh JWT **access token**.\n\n"
        "### 🔓 Access\n"
        "- **Public endpoint**\n"
        "- Used when access token expires\n\n"
        "### 🔁 Behavior\n"
        "- Requires a **valid refresh token**\n"
        "- Returns a new access token\n\n"
        "### 📥 Example Request Body\n"
        "```json\n"
        "{\n"
        '  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."\n'
        "}\n"
        "```"
    ),
    responses={
        200: {
            "description": "New access token generated",
            "content": {
                "application/json": {
                    "example": {"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
                }
            },
        },
        401: {"description": "Invalid or expired refresh token"},
    },
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    tags=["Authentication"],
    summary="Blacklist JWT Refresh Token (Logout)",
    description=(
        "Blacklist a JWT refresh token to log out the user.\n\n"
        "### 🔐 Access\n"
        "- Requires valid **JWT access token**\n\n"
        "### 🗑 Behavior\n"
        "- Invalidates the provided refresh token, preventing further use.\n"
        "- The access token remains valid until its expiration.\n\n"
        "### 📥 Example Request Body\n"
        "```json\n"
        "{\n"
        '  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."\n'
        "}\n"
        "```"
    ),
    responses={
        200: {"description": "Successfully logged out."},
        401: {"description": "Authentication required or invalid token."},
    },
)
class LogoutView(TokenBlacklistView):
    permission_classes = (permissions.IsAuthenticated,)


@extend_schema(
    tags=["Authentication"],
    summary="Register a New Job Seeker Account",
    description=(
        "Register as a **Job Seeker**.\n\n"
        "### 🔓 Access\n"
        "- **Public endpoint** (no authentication required)\n\n"
        "### 👤 Role Assignment\n"
        "- Automatically assigns **JOB_SEEKER** role\n"
        "- **ADMIN** and **EMPLOYER** roles require admin privileges\n\n"
        "### ✅ Required Fields\n"
        "- username (unique)\n"
        "- email (unique, validated)\n"
        "- password (minimum 8 characters, write-only)\n\n"
        "### ➕ Optional Fields\n"
        "- first_name\n"
        "- last_name\n\n"
        "### 📥 Example Request Body\n"
        "```json\n"
        "{\n"
        '  "username": "job_seeker1",\n'
        '  "email": "seeker@example.com",\n'
        '  "password": "SecurePass123",\n'
        '  "first_name": "John",\n'
        '  "last_name": "Doe"\n'
        "}\n"
        "```"
    ),
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "job_seeker1",
                        "email": "seeker@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "role": "JOB_SEEKER",
                    }
                }
            },
        },
        400: {
            "description": "Validation error (duplicate username/email, weak password)"
        },
    },
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# =========================
# User Profile
# =========================


@extend_schema(
    tags=["User Profile"],
    summary="Manage Authenticated User Profile",
    description=(
        "Authenticated user profile management.\n\n"
        "### 🔐 Access\n"
        "- Requires valid **JWT access token**\n\n"
        "### 📌 Supported Operations\n"
        "- **GET**: Retrieve your profile\n"
        "- **PATCH**: Update your profile (partial updates)\n"
        "- **DELETE**: Deactivate your account (soft delete)"
    ),
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Account is deactivated"},
    },
)
class ProfileView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer  # default serializer for GET responses

    @extend_schema(
        summary="Retrieve Authenticated User Profile",
        description=(
            "Retrieve authenticated user's profile.\n\n"
            "### 📄 Response Includes\n"
            "- id, username, email\n"
            "- first_name, last_name\n"
            "- role\n\n"
            "⚠️ Sensitive fields (e.g. password) are never exposed."
        ),
        responses={200: UserSerializer},
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        request=ProfileUpdateSerializer,
        summary="Update Authenticated User Profile",
        description=(
            "Update your profile information.\n\n"
            "### ✏️ Updatable Fields\n"
            "- first_name\n"
            "- last_name\n"
            "- email (must remain unique)\n\n"
            "### 🚫 Restricted Fields\n"
            "- username\n"
            "- role\n\n"
            "### 📥 Example Request Body\n"
            "```json\n"
            "{\n"
            '  "first_name": "UpdatedFirstName",\n'
            '  "last_name": "UpdatedLastName",\n'
            '  "email": "newemail@example.com"\n'
            "}\n"
            "```"
        ),
        responses={
            200: UserSerializer,
            400: {"description": "Validation error"},
        },
    )
    def patch(self, request, *args, **kwargs):
        serializer = ProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    @extend_schema(
        summary="Deactivate Authenticated User Account",
        description=(
            "Deactivate your account.\n\n"
            "### 🧹 Behavior\n"
            "- Soft delete (sets `is_active = False`)\n"
            "- Login is disabled\n"
            "- Data is preserved\n\n"
            "⚠️ Reactivation requires admin action."
        ),
        responses={204: {"description": "Account deactivated"}},
    )
    def delete(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["User Profile"],
    summary="Change User Password",
    description=(
        "Allows an authenticated user to change their password.\n\n"
        "### 🔐 Access\n"
        "- Requires valid **JWT access token**\n\n"
        "### 📥 Example Request Body\n"
        "```json\n"
        "{\n"
        '  "old_password": "oldsecurepassword123",\n'
        '  "new_password": "newsecurepassword123",\n'
        '  "confirm_new_password": "newsecurepassword123"\n'
        "}\n"
        "```"
    ),
    request=ChangePasswordSerializer,
    responses={
        200: {"description": "Password updated successfully."},
        400: {"description": "Invalid data or old password mismatch."},
        401: {"description": "Authentication required."},
    },
)
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password automatically
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "Password updated successfully."} ,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# Admin Management
# =========================


@extend_schema(
    tags=["Admin Management"],
    summary="Admin-only User Management",
    description=(
        "Admin-only user management.\n\n"
        "### 🔐 Access\n"
        "- Requires **ADMIN** role\n\n"
        "### 🛠 Capabilities\n"
        "- Create users with any role\n"
        "- List all users\n"
        "- Update or delete accounts\n"
        "- Reactivate deactivated users"
    ),
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin privileges required"},
    },
)
class AdminUserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


@extend_schema(
    tags=["Admin Management"],
    summary="Admin-only User Detail Operations",
    description=(
        "Admin user detail operations.\n\n"
        "### 🔐 Access\n"
        "- Requires **ADMIN** role\n\n"
        "### 📌 Supported Operations\n"
        "- GET, PUT, PATCH, DELETE\n\n"
        "⚠️ DELETE permanently removes the user."
    ),
)
class AdminUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

