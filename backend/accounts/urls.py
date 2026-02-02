from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)
from .views import RegisterView, ProfileView



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
