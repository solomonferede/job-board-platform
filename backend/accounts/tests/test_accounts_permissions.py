import pytest
from rest_framework.test import APIRequestFactory
from accounts.permissions import IsAdmin, IsEmployer
from accounts.tests.factories import JobSeekerUserFactory, EmployerUserFactory, AdminUserFactory


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.mark.django_db
class TestIsAdminPermission:
    def test_admin_user_has_permission(self, request_factory):
        admin_user = AdminUserFactory()
        request = request_factory.get("/")
        request.user = admin_user
        permission = IsAdmin()
        assert permission.has_permission(request, None) is True

    def test_employer_user_no_permission(self, request_factory):
        employer_user = EmployerUserFactory()
        request = request_factory.get("/")
        request.user = employer_user
        permission = IsAdmin()
        assert permission.has_permission(request, None) is False

    def test_job_seeker_user_no_permission(self, request_factory):
        job_seeker_user = JobSeekerUserFactory()
        request = request_factory.get("/")
        request.user = job_seeker_user
        permission = IsAdmin()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_user_no_permission(self, request_factory):
        request = request_factory.get("/")
        request.user = None  # Unauthenticated user
        permission = IsAdmin()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsEmployerPermission:
    def test_employer_user_has_permission(self, request_factory):
        employer_user = EmployerUserFactory()
        request = request_factory.get("/")
        request.user = employer_user
        permission = IsEmployer()
        assert permission.has_permission(request, None) is True

    def test_admin_user_has_permission(self, request_factory):
        admin_user = AdminUserFactory()
        request = request_factory.get("/")
        request.user = admin_user
        permission = IsEmployer()
        # Admins are also employers in this context if they have a company profile
        # However, the permission only checks is_employer flag.
        # If an admin is not explicitly marked as is_employer, this should be False.
        # Let's assume AdminUserFactory does not set is_employer by default.
        assert permission.has_permission(request, None) is False

    def test_job_seeker_user_no_permission(self, request_factory):
        job_seeker_user = JobSeekerUserFactory()
        request = request_factory.get("/")
        request.user = job_seeker_user
        permission = IsEmployer()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_user_no_permission(self, request_factory):
        request = request_factory.get("/")
        request.user = None  # Unauthenticated user
        permission = IsEmployer()
        assert permission.has_permission(request, None) is False
