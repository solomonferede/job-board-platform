import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

BASE_URL = "/api/v1/accounts"


# ==========================
# FIXTURES
# ==========================


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def job_seeker(db):
    return User.objects.create_user(
        username="jobseeker",
        email="jobseeker@test.com",
        password="StrongPass123!",
        role=User.Role.JOB_SEEKER,
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="AdminPass123!",
    )


@pytest.fixture
def employer(db):
    return User.objects.create_user(
        username="employer",
        email="employer@test.com",
        password="EmployerPass123!",
        role=User.Role.EMPLOYER,
    )


@pytest.fixture
def auth_client(api_client, job_seeker):
    api_client.force_authenticate(user=job_seeker)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


# ==========================
# AUTHENTICATION TESTS
# ==========================


@pytest.mark.django_db
def test_register_job_seeker_success(api_client):
    payload = {
        "username": "newuser",
        "email": "newuser@test.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
        "first_name": "New",
        "last_name": "User",
    }

    response = api_client.post(f"{BASE_URL}/register/", payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"
    assert User.objects.get(username="newuser").role == User.Role.JOB_SEEKER


@pytest.mark.django_db
def test_register_password_mismatch(api_client):
    payload = {
        "username": "baduser",
        "email": "bad@test.com",
        "password": "StrongPass123!",
        "confirm_password": "WrongPass123!",
    }

    response = api_client.post(f"{BASE_URL}/register/", payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


@pytest.mark.django_db
def test_token_obtain_pair_success(api_client, job_seeker):
    payload = {
        "username": "jobseeker",
        "password": "StrongPass123!",
    }

    response = api_client.post(f"{BASE_URL}/token/", payload)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_refresh(api_client, job_seeker):
    token_response = api_client.post(
        f"{BASE_URL}/token/",
        {"username": "jobseeker", "password": "StrongPass123!"},
    )

    refresh = token_response.data["refresh"]

    response = api_client.post(
        f"{BASE_URL}/token/refresh/",
        {"refresh": refresh},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_logout_blacklist_refresh_token(api_client, job_seeker):
    token_response = api_client.post(
        f"{BASE_URL}/token/",
        {"username": "jobseeker", "password": "StrongPass123!"},
    )

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")

    response = api_client.post(
        f"{BASE_URL}/logout/",
        {"refresh": token_response.data["refresh"]},
    )

    assert response.status_code == status.HTTP_200_OK


# ==========================
# PROFILE TESTS
# ==========================


@pytest.mark.django_db
def test_get_profile(auth_client):
    response = auth_client.get(f"{BASE_URL}/profile/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "jobseeker"


@pytest.mark.django_db
def test_update_profile(auth_client):
    response = auth_client.patch(
        f"{BASE_URL}/profile/",
        {"first_name": "Updated"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Updated"


@pytest.mark.django_db
def test_delete_profile(auth_client):
    response = auth_client.delete(f"{BASE_URL}/profile/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    user = User.objects.get(username="jobseeker")
    assert user.is_active is False


@pytest.mark.django_db
def test_profile_requires_authentication(api_client):
    response = api_client.get(f"{BASE_URL}/profile/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ==========================
# PASSWORD CHANGE TESTS
# ==========================


@pytest.mark.django_db
def test_change_password_success(auth_client, job_seeker):
    payload = {
        "old_password": "StrongPass123!",
        "new_password": "NewStrongPass123!",
        "confirm_new_password": "NewStrongPass123!",
    }

    response = auth_client.patch(f"{BASE_URL}/change-password/", payload)

    assert response.status_code == status.HTTP_200_OK

    job_seeker.refresh_from_db()
    assert job_seeker.check_password("NewStrongPass123!")


@pytest.mark.django_db
def test_change_password_wrong_old(auth_client):
    payload = {
        "old_password": "WrongPass",
        "new_password": "AnotherStrong123!",
        "confirm_new_password": "AnotherStrong123!",
    }

    response = auth_client.patch(f"{BASE_URL}/change-password/", payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "old_password" in response.data


# ==========================
# ADMIN MANAGEMENT TESTS
# ==========================


@pytest.mark.django_db
def test_admin_list_users(admin_client):
    response = admin_client.get(f"{BASE_URL}/admin/users/")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_non_admin_cannot_list_users(auth_client):
    response = auth_client.get(f"{BASE_URL}/admin/users/")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_retrieve_user(admin_client, job_seeker):
    response = admin_client.get(f"{BASE_URL}/admin/users/{job_seeker.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "jobseeker"


@pytest.mark.django_db
def test_admin_update_user(admin_client, job_seeker):
    response = admin_client.patch(
        f"{BASE_URL}/admin/users/{job_seeker.id}/",
        {"is_active": False},
    )

    assert response.status_code == status.HTTP_200_OK
    job_seeker.refresh_from_db()
    assert job_seeker.is_active is False


@pytest.mark.django_db
def test_admin_delete_user(admin_client, job_seeker):
    response = admin_client.delete(f"{BASE_URL}/admin/users/{job_seeker.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=job_seeker.id).exists()
