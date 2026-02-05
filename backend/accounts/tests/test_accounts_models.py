import pytest
from accounts.tests.factories import (
    AdminUserFactory,
    JobSeekerUserFactory,
)
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestAuthenticationEndpoints:
    def test_register_job_seeker_success(self):
        client = APIClient()
        payload = {
            "username": "jobseeker1",
            "email": "jobseeker@example.com",
            "password": "StrongPass123",
        }

        response = client.post("/api/v1/accounts/auth/register/", payload)
        assert response.status_code == 201
        assert response.data["username"] == "jobseeker1"

    def test_login_success(self):
        user = JobSeekerUserFactory(username="john")
        client = APIClient()

        response = client.post(
            "/api/v1/accounts/auth/login/",
            {"username": "john", "password": "password123"},
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self):
        client = APIClient()
        response = client.post(
            "/api/v1/accounts/auth/login/",
            {"username": "wrong", "password": "wrong"},
        )
        assert response.status_code == 401

    def test_logout_success(self):
        user = JobSeekerUserFactory(username="logoutuser")
        client = APIClient()

        login = client.post(
            "/api/v1/accounts/auth/login/",
            {"username": "logoutuser", "password": "password123"},
        )
        access = login.data["access"]
        refresh = login.data["refresh"]

        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = client.post("/api/v1/accounts/auth/logout/", {"refresh": refresh})

        assert response.status_code == 200


class TestProfileEndpoints:
    def test_profile_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/v1/accounts/me/")
        assert response.status_code == 401

    def test_profile_authenticated(self):
        user = JobSeekerUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/accounts/me/")
        assert response.status_code == 200
        assert response.data["username"] == user.username

    def test_change_password_success(self):
        user = JobSeekerUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.put(
            "/api/v1/accounts/me/change-password/",
            {
                "old_password": "password123",
                "new_password": "NewStrongPass123",
                "confirm_new_password": "NewStrongPass123",
            },
        )

        assert response.status_code == 200


class TestAdminEndpoints:
    def test_admin_can_list_users(self):
        admin = AdminUserFactory()
        client = APIClient()
        client.force_authenticate(user=admin)

        response = client.get("/api/v1/accounts/admin/users/")
        assert response.status_code == 200
