import pytest
from django.contrib.auth import get_user_model
from jobs.models import Company # Import Company from jobs app
from accounts.tests.factories import (
    JobSeekerUserFactory,
    EmployerUserFactory,
    AdminUserFactory,
    UserFactory,
)
from jobs.tests.factories import CompanyFactory


User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = UserFactory(email="test@example.com", password="password123")
        assert user.email == "test@example.com"
        assert user.check_password("password123")
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active
        assert user.role == User.Role.JOB_SEEKER # Default role

    def test_create_job_seeker_user(self):
        user = JobSeekerUserFactory(email="jobseeker@example.com")
        assert user.role == User.Role.JOB_SEEKER
        assert user.is_job_seeker()
        assert not user.is_employer()
        assert user.company is None

    def test_create_employer_user(self):
        user = EmployerUserFactory(email="employer@example.com")
        assert user.role == User.Role.EMPLOYER
        assert user.is_employer()
        assert not user.is_job_seeker()
        assert user.company is not None
        assert isinstance(user.company, Company)

    def test_create_admin_user(self):
        user = AdminUserFactory(email="admin@example.com")
        assert user.role == User.Role.ADMIN
        assert user.is_staff
        assert user.is_superuser
        assert user.is_admin()

    def test_user_str_representation(self):
        user = UserFactory(email="strtest@example.com", first_name="Test", last_name="User")
        assert str(user) == "Test User (strtest@example.com)"

    def test_employer_user_company_relationship(self):
        employer = EmployerUserFactory()
        assert employer.company is not None
        assert employer.company.created_by == employer

    def test_job_seeker_profile_methods(self):
        job_seeker = JobSeekerUserFactory()
        assert job_seeker.is_job_seeker()
        assert not job_seeker.is_employer()
        assert not job_seeker.is_admin()

    def test_employer_profile_methods(self):
        employer = EmployerUserFactory()
        assert employer.is_employer()
        assert not employer.is_job_seeker()
        assert not employer.is_admin()

    def test_admin_profile_methods(self):
        admin_user = AdminUserFactory()
        assert admin_user.is_admin()
        assert not admin_user.is_job_seeker()
        assert not admin_user.is_employer()