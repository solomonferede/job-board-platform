import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from applications.models import Application
from accounts.tests.factories import JobSeekerUserFactory, EmployerUserFactory, AdminUserFactory
from jobs.tests.factories import JobFactory
from applications.tests.factories import ApplicationFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def job_seeker_user():
    return JobSeekerUserFactory()


@pytest.fixture
def employer_user():
    return EmployerUserFactory()


@pytest.fixture
def admin_user():
    return AdminUserFactory()


@pytest.fixture
def authenticated_job_seeker(api_client, job_seeker_user):
    api_client.force_authenticate(user=job_seeker_user)
    return api_client, job_seeker_user


@pytest.fixture
def authenticated_employer(api_client, employer_user):
    api_client.force_authenticate(user=employer_user)
    return api_client, employer_user


@pytest.fixture
def authenticated_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client, admin_user


@pytest.mark.django_db
class TestMyApplicationListView:
    list_url = reverse("my-application-list")

    def test_job_seeker_can_list_their_applications(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        ApplicationFactory.create_batch(3, applicant=job_seeker)
        ApplicationFactory.create_batch(2)  # Other applications
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3
        for app_data in response.data["results"]:
            assert app_data["applicant"] == str(job_seeker)

    def test_employer_cannot_list_my_applications(self, authenticated_employer):
        api_client, _ = authenticated_employer
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_list_my_applications(self, api_client):
        response = api_client.get(self.list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestApplicationDetailView:
    def test_applicant_can_retrieve_their_application(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        application = ApplicationFactory(applicant=job_seeker)
        url = reverse("application-detail", kwargs={"pk": application.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == application.pk

    def test_employer_can_retrieve_application_for_their_job(self, authenticated_employer):
        api_client, employer = authenticated_employer
        job = JobFactory(created_by=employer)
        application = ApplicationFactory(job=job)
        url = reverse("application-detail", kwargs={"pk": application.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == application.pk

    def test_employer_cannot_retrieve_application_for_other_job(self, authenticated_employer):
        api_client, _ = authenticated_employer
        application = ApplicationFactory()  # Job created by another employer
        url = reverse("application-detail", kwargs={"pk": application.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_retrieve_any_application(self, authenticated_admin):
        api_client, _ = authenticated_admin
        application = ApplicationFactory()
        url = reverse("application-detail", kwargs={"pk": application.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == application.pk

    def test_applicant_can_withdraw_their_application(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        application = ApplicationFactory(applicant=job_seeker)
        url = reverse("application-detail", kwargs={"pk": application.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK  # DELETE performs a soft delete (status change)
        application.refresh_from_db()
        assert application.status == Application.Status.WITHDRAWN

    def test_employer_cannot_withdraw_application(self, authenticated_employer):
        api_client, _ = authenticated_employer
        application = ApplicationFactory()
        url = reverse("application-detail", kwargs={"pk": application.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_employer_can_update_application_status_for_their_job(self, authenticated_employer):
        api_client, employer = authenticated_employer
        job = JobFactory(created_by=employer)
        application = ApplicationFactory(job=job, status=Application.Status.PENDING)
        url = reverse("application-detail", kwargs={"pk": application.pk})
        data = {"status": Application.Status.REVIEWED}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        application.refresh_from_db()
        assert application.status == Application.Status.REVIEWED

    def test_applicant_cannot_update_application_status(self, authenticated_job_seeker):
        api_client, job_seeker = authenticated_job_seeker
        application = ApplicationFactory(applicant=job_seeker, status=Application.Status.PENDING)
        url = reverse("application-detail", kwargs={"pk": application.pk})
        data = {"status": Application.Status.REVIEWED}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_application_status(self, authenticated_admin):
        api_client, _ = authenticated_admin
        application = ApplicationFactory(status=Application.Status.PENDING)
        url = reverse("application-detail", kwargs={"pk": application.pk})
        data = {"status": Application.Status.ACCEPTED}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        application.refresh_from_db()
        assert application.status == Application.Status.ACCEPTED