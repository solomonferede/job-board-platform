"""
backend.accounts.urls module which contains URL patterns for user registration,
login, token refresh, and profile management.
"""

from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
