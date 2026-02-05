import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from jobs.models import Category, JobType, Location, Company, Job
from accounts.tests.factories import EmployerUserFactory, JobSeekerUserFactory, AdminUserFactory
from jobs.tests.factories import (
    CategoryFactory,
    JobTypeFactory,
    LocationFactory,
    CompanyFactory,
    JobFactory,
)
from applications.tests.factories import ApplicationFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def employer_user():
    return EmployerUserFactory()


@pytest.fixture
def job_seeker_user():
    return JobSeekerUserFactory()


@pytest.fixture
def admin_user():
    return AdminUserFactory()


@pytest.fixture
def authenticated_employer(api_client, employer_user):
    api_client.force_authenticate(user=employer_user)
    return api_client, employer_user


@pytest.fixture
def authenticated_job_seeker(api_client, job_seeker_user):
    api_client.force_authenticate(user=job_seeker_user)
    return api_client, job_seeker_user


@pytest.fixture
def authenticated_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client, admin_user


@pytest.mark.django_db
class TestCategoryViewSet:
    list_url = reverse("category-list-create")

    def test_list_categories(self, api_client):
        CategoryFactory.create_batch(3)
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_category_by_admin(self, authenticated_admin):
        api_client, _ = authenticated_admin
        data = {"name": "New Category"}
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Category").exists()

    def test_create_category_by_employer_forbidden(self, authenticated_employer):
        api_client, _ = authenticated_employer
        data = {"name": "New Category"}
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_category(self, api_client):
        category = CategoryFactory()
        url = reverse("category-detail", kwargs={"id": category.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category.name

    def test_update_category_by_admin(self, authenticated_admin):
        api_client, _ = authenticated_admin
        category = CategoryFactory()
        url = reverse("category-detail", kwargs={"id": category.pk})
        data = {"name": "Updated Category"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == "Updated Category"

    def test_delete_category_by_admin(self, authenticated_admin):
        api_client, _ = authenticated_admin
        category = CategoryFactory()
        url = reverse("category-detail", kwargs={"id": category.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
class TestJobTypeViewSet:
    list_url = reverse("jobtype-list-create")

    def test_list_job_types(self, api_client):
        JobTypeFactory.create_batch(3)
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_job_type_by_admin(self, authenticated_admin):
        api_client, _ = authenticated_admin
        data = {"name": "Full-time"}
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert JobType.objects.filter(name="Full-time").exists()

    def test_retrieve_job_type(self, api_client):
        job_type = JobTypeFactory()
        url = reverse("jobtype-detail", kwargs={"id": job_type.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == job_type.name


@pytest.mark.django_db
class TestLocationViewSet:
    list_url = reverse("location-list-create")

    def test_list_locations(self, api_client):
        LocationFactory.create_batch(3)
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_location_by_admin(self, authenticated_admin):
        api_client, _ = authenticated_admin
        data = {"name": "Remote"}
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Location.objects.filter(name="Remote").exists()

    def test_retrieve_location(self, api_client):
        location = LocationFactory()
        url = reverse("location-detail", kwargs={"id": location.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == location.name


@pytest.mark.django_db
class TestCompanyViewSet:
    list_url = reverse("company-list-create")

    def test_list_companies(self, api_client):
        CompanyFactory.create_batch(3)
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_company_by_employer(self, authenticated_employer):
        api_client, employer = authenticated_employer
        data = {
            "name": "Employer Company",
            "description": "Desc",
            "website": "http://employer.com",
        }
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Company.objects.filter(name="Employer Company").exists()
        assert Company.objects.get(name="Employer Company").created_by == employer

    def test_retrieve_company(self, api_client):
        company = CompanyFactory()
        url = reverse("company-detail", kwargs={"id": company.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == company.name

    def test_update_company_by_owner(self, authenticated_employer):
        api_client, employer = authenticated_employer
        company = CompanyFactory(created_by=employer)
        url = reverse("company-detail", kwargs={"id": company.pk})
        data = {"name": "Updated Employer Company"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        company.refresh_from_db()
        assert company.name == "Updated Employer Company"

    def test_update_company_by_non_owner_forbidden(self, authenticated_employer):
        api_client, _ = authenticated_employer
        company = CompanyFactory()  # Created by another employer
        url = reverse("company-detail", kwargs={"id": company.pk})
        data = {"name": "Updated Employer Company"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestJobViewSet:
    list_url = reverse("job-list-create")

    def test_list_jobs(self, api_client):
        JobFactory.create_batch(3)
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_create_job_by_employer(self, authenticated_employer):
        api_client, employer = authenticated_employer
        company = CompanyFactory(created_by=employer)
        category = CategoryFactory()
        job_type = JobTypeFactory()
        location = LocationFactory()

        data = {
            "title": "Software Engineer",
            "description": "Develop software",
            "requirements": "BS in CS",
            "salary": 100000,
            "company": company.pk,
            "category": category.pk,
            "job_type": job_type.pk,
            "location": location.pk,
            "skills": ["Python", "Django"],
        }
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Job.objects.filter(title="Software Engineer").exists()
        job = Job.objects.get(title="Software Engineer")
        assert job.created_by == employer
        assert job.skills.count() == 2

    def test_create_job_by_job_seeker_forbidden(self, authenticated_job_seeker):
        api_client, _ = authenticated_job_seeker
        company = CompanyFactory()
        category = CategoryFactory()
        job_type = JobTypeFactory()
        location = LocationFactory()

        data = {
            "title": "Software Engineer",
            "description": "Develop software",
            "requirements": "BS in CS",
            "salary": 100000,
            "company": company.pk,
            "category": category.pk,
            "job_type": job_type.pk,
            "location": location.pk,
            "skills": ["Python", "Django"],
        }
        response = api_client.post(self.list_url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_job(self, api_client):
        job = JobFactory()
        url = reverse("job-detail", kwargs={"id": job.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == job.title

    def test_update_job_by_owner(self, authenticated_employer):
        api_client, employer = authenticated_employer
        job = JobFactory(created_by=employer)
        url = reverse("job-detail", kwargs={"id": job.pk})
        data = {"title": "Updated Software Engineer"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        job.refresh_from_db()
        assert job.title == "Updated Software Engineer"

    def test_delete_job_by_owner(self, authenticated_employer):
        api_client, employer = authenticated_employer
        job = JobFactory(created_by=employer)
        url = reverse("job-detail", kwargs={"id": job.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Job.objects.filter(pk=job.pk).exists()


@pytest.mark.django_db
class TestJobApplicationListCreateView:
    def test_job_seeker_can_apply_to_job(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        job = JobFactory()
        url = reverse("job-application-list-create", kwargs={"job_pk": job.pk})
        data = {
            "cover_letter": "My cover letter",
            "resume": "http://example.com/resume.pdf",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["applicant"] == str(job_seeker)
        assert response.data["job"] == str(job)

    def test_job_seeker_cannot_apply_twice(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        job = JobFactory()
        ApplicationFactory(applicant=job_seeker, job=job)
        url = reverse("job-application-list-create", kwargs={"job_pk": job.pk})
        data = {
            "cover_letter": "My cover letter",
            "resume": "http://example.com/resume.pdf",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "You have already applied to this job." in response.data["non_field_errors"]

    def test_employer_cannot_apply_to_job(self, authenticated_employer):
        api_client, _ = authenticated_employer
        job = JobFactory()
        url = reverse("job-application-list-create", kwargs={"job_pk": job.pk})
        data = {
            "cover_letter": "My cover letter",
            "resume": "http://example.com/resume.pdf",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_employer_can_list_applications_for_their_job(self, authenticated_employer):
        api_client, employer = authenticated_employer
        job = JobFactory(created_by=employer)
        ApplicationFactory.create_batch(3, job=job)
        url = reverse("job-application-list-create", kwargs={"job_pk": job.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3

    def test_employer_cannot_list_applications_for_other_job(self, authenticated_employer):
        api_client, _ = authenticated_employer
        job = JobFactory()  # Created by another employer
        ApplicationFactory.create_batch(3, job=job)
        url = reverse("job-application-list-create", kwargs={"job_pk": job.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_job_seeker_can_list_only_their_application_for_a_job(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        job = JobFactory()
        ApplicationFactory(applicant=job_seeker, job=job)  # Job seeker's application
        ApplicationFactory.create_batch(2, job=job)  # Other applications
        url = reverse("job-application-list-create", kwargs={"job_pk": job.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["applicant"] == str(job_seeker)
