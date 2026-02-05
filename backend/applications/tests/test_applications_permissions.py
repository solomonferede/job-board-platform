import pytest
from rest_framework.test import APIRequestFactory
from applications.permissions import (
    IsApplicantOwner,
    IsJobSeeker,
    IsEmployer,
    IsAdmin,
    IsJobOwner,
)
from accounts.tests.factories import (
    JobSeekerUserFactory,
    EmployerUserFactory,
    AdminUserFactory,
    UserFactory,
)
from applications.tests.factories import ApplicationFactory
from jobs.tests.factories import JobFactory


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.mark.django_db
class TestIsApplicantOwnerPermission:
    def test_owner_has_object_permission(self, request_factory):
        applicant = JobSeekerUserFactory()
        application = ApplicationFactory(applicant=applicant)
        request = request_factory.get("/")
        request.user = applicant
        permission = IsApplicantOwner()
        assert permission.has_object_permission(request, None, application) is True

    def test_non_owner_no_object_permission(self, request_factory):
        applicant = JobSeekerUserFactory()
        non_owner = JobSeekerUserFactory()
        application = ApplicationFactory(applicant=applicant)
        request = request_factory.get("/")
        request.user = non_owner
        permission = IsApplicantOwner()
        assert permission.has_object_permission(request, None, application) is False


@pytest.mark.django_db
class TestIsJobSeekerPermission:
    def test_job_seeker_has_permission(self, request_factory):
        job_seeker = JobSeekerUserFactory()
        request = request_factory.get("/")
        request.user = job_seeker
        permission = IsJobSeeker()
        assert permission.has_permission(request, None) is True

    def test_employer_no_permission(self, request_factory):
        employer = EmployerUserFactory()
        request = request_factory.get("/")
        request.user = employer
        permission = IsJobSeeker()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_no_permission(self, request_factory):
        request = request_factory.get("/")
        request.user = None
        permission = IsJobSeeker()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsEmployerPermission:
    def test_employer_has_permission(self, request_factory):
        employer = EmployerUserFactory()
        request = request_factory.get("/")
        request.user = employer
        permission = IsEmployer()
        assert permission.has_permission(request, None) is True

    def test_job_seeker_no_permission(self, request_factory):
        job_seeker = JobSeekerUserFactory()
        request = request_factory.get("/")
        request.user = job_seeker
        permission = IsEmployer()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsAdminPermission:
    def test_admin_has_permission(self, request_factory):
        admin_user = AdminUserFactory()
        request = request_factory.get("/")
        request.user = admin_user
        permission = IsAdmin()
        assert permission.has_permission(request, None) is True

    def test_non_admin_no_permission(self, request_factory):
        job_seeker = JobSeekerUserFactory()
        request = request_factory.get("/")
        request.user = job_seeker
        permission = IsAdmin()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsJobOwnerPermission:
    def test_has_permission_for_list_view_owner(self, request_factory):
        employer = EmployerUserFactory()
        job = JobFactory(created_by=employer)
        request = request_factory.get("/")
        request.user = employer
        view = type("View", (object,), {"kwargs": {"job_pk": job.pk}})()
        permission = IsJobOwner()
        assert permission.has_permission(request, view) is True

    def test_has_permission_for_list_view_non_owner(self, request_factory):
        employer = EmployerUserFactory()
        job = JobFactory()  # Created by another employer
        request = request_factory.get("/")
        request.user = employer
        view = type("View", (object,), {"kwargs": {"job_pk": job.pk}})()
        permission = IsJobOwner()
        assert permission.has_permission(request, view) is False

    def test_has_object_permission_owner(self, request_factory):
        employer = EmployerUserFactory()
        job = JobFactory(created_by=employer)
        application = ApplicationFactory(job=job)
        request = request_factory.get("/")
        request.user = employer
        permission = IsJobOwner()
        assert permission.has_object_permission(request, None, application) is True

    def test_has_object_permission_non_owner(self, request_factory):
        employer = EmployerUserFactory()
        job = JobFactory()  # Created by another employer
        application = ApplicationFactory(job=job)
        request = request_factory.get("/")
        request.user = employer
        permission = IsJobOwner()
        assert permission.has_object_permission(request, None, application) is False
