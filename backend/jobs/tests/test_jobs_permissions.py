import pytest
from rest_framework.test import APIRequestFactory
from rest_framework import permissions
from jobs.permissions import (
    IsAdminOrReadOnly,
    IsAdminOrOwnerOrReadOnly,
    IsAdminOrEmployer,
    IsAdminOrResourceOwner,
)
from accounts.tests.factories import (
    JobSeekerUserFactory,
    EmployerUserFactory,
    AdminUserFactory,
    UserFactory,
)
from jobs.tests.factories import JobFactory, CompanyFactory


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.mark.django_db
class TestIsAdminOrReadOnlyPermission:
    def test_safe_method_allowed_for_any_user(self, request_factory):
        request = request_factory.get("/")
        request.user = UserFactory()  # Any authenticated user
        permission = IsAdminOrReadOnly()
        assert permission.has_permission(request, None) is True

    def test_post_method_allowed_for_admin(self, request_factory):
        admin_user = AdminUserFactory()
        request = request_factory.post("/")
        request.user = admin_user
        permission = IsAdminOrReadOnly()
        assert permission.has_permission(request, None) is True

    def test_post_method_forbidden_for_non_admin(self, request_factory):
        employer_user = EmployerUserFactory()
        request = request_factory.post("/")
        request.user = employer_user
        permission = IsAdminOrReadOnly()
        assert permission.has_permission(request, None) is False

    def test_post_method_forbidden_for_unauthenticated(self, request_factory):
        request = request_factory.post("/")
        request.user = None  # Unauthenticated user
        permission = IsAdminOrReadOnly()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsAdminOrOwnerOrReadOnlyPermission:
    def test_safe_method_allowed_for_any_user(self, request_factory):
        request = request_factory.get("/")
        request.user = UserFactory()
        permission = IsAdminOrOwnerOrReadOnly()
        assert permission.has_permission(request, None) is True

    def test_post_method_allowed_for_authenticated(self, request_factory):
        employer_user = EmployerUserFactory()
        request = request_factory.post("/")
        request.user = employer_user
        permission = IsAdminOrOwnerOrReadOnly()
        assert permission.has_permission(request, None) is True

    def test_post_method_forbidden_for_unauthenticated(self, request_factory):
        request = request_factory.post("/")
        request.user = None
        permission = IsAdminOrOwnerOrReadOnly()
        assert permission.has_permission(request, None) is False

    def test_object_permission_owner_allowed(self, request_factory):
        employer_user = EmployerUserFactory()
        company = CompanyFactory(created_by=employer_user)
        request = request_factory.patch("/")
        request.user = employer_user
        permission = IsAdminOrOwnerOrReadOnly()
        assert permission.has_object_permission(request, None, company) is True

    def test_object_permission_admin_allowed(self, request_factory):
        admin_user = AdminUserFactory()
        company = CompanyFactory()  # Created by another user
        request = request_factory.patch("/")
        request.user = admin_user
        permission = IsAdminOrOwnerOrReadOnly()
        assert permission.has_object_permission(request, None, company) is True

    def test_object_permission_non_owner_forbidden(self, request_factory):
        employer_user = EmployerUserFactory()
        company = CompanyFactory()  # Created by another user
        request = request_factory.patch("/")
        request.user = employer_user
        permission = IsAdminOrOwnerOrReadOnly()
        assert permission.has_object_permission(request, None, company) is False


@pytest.mark.django_db
class TestIsAdminOrEmployerPermission:
    def test_admin_allowed(self, request_factory):
        admin_user = AdminUserFactory()
        request = request_factory.get("/")
        request.user = admin_user
        permission = IsAdminOrEmployer()
        assert permission.has_permission(request, None) is True

    def test_employer_allowed(self, request_factory):
        employer_user = EmployerUserFactory()
        request = request_factory.get("/")
        request.user = employer_user
        permission = IsAdminOrEmployer()
        assert permission.has_permission(request, None) is True

    def test_job_seeker_forbidden(self, request_factory):
        job_seeker_user = JobSeekerUserFactory()
        request = request_factory.get("/")
        request.user = job_seeker_user
        permission = IsAdminOrEmployer()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_forbidden(self, request_factory):
        request = request_factory.get("/")
        request.user = None
        permission = IsAdminOrEmployer()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsAdminOrResourceOwnerPermission:
    def test_object_permission_owner_allowed(self, request_factory):
        employer_user = EmployerUserFactory()
        job = JobFactory(created_by=employer_user)
        request = request_factory.patch("/")
        request.user = employer_user
        permission = IsAdminOrResourceOwner()
        assert permission.has_object_permission(request, None, job) is True

    def test_object_permission_admin_allowed(self, request_factory):
        admin_user = AdminUserFactory()
        job = JobFactory()  # Created by another user
        request = request_factory.patch("/")
        request.user = admin_user
        permission = IsAdminOrResourceOwner()
        assert permission.has_object_permission(request, None, job) is True

    def test_object_permission_non_owner_forbidden(self, request_factory):
        employer_user = EmployerUserFactory()
        job = JobFactory()  # Created by another user
        request = request_factory.patch("/")
        request.user = employer_user
        permission = IsAdminOrResourceOwner()
        assert permission.has_object_permission(request, None, job) is False
