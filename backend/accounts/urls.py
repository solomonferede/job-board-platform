"""
backend.accounts.urls module which contains URL patterns for user registration,
login, token refresh, and profile management.
"""

from django.urls import path

from .views import (
    AdminUserListCreateView,
    AdminUserRetrieveUpdateDestroyView,
    ChangePasswordView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "admin/users/", AdminUserListCreateView.as_view(), name="admin-user-list-create"
    ),
    path(
        "admin/users/<int:pk>/",
        AdminUserRetrieveUpdateDestroyView.as_view(),
        name="admin-user-detail",
    ),
]
