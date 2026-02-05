import pytest
from applications.models import Application
from applications.tests.factories import ApplicationFactory
from jobs.tests.factories import JobFactory
from accounts.tests.factories import JobSeekerUserFactory


@pytest.mark.django_db
class TestApplicationModel:
    def test_create_application(self):
        job_seeker = JobSeekerUserFactory()
        job = JobFactory()
        application = ApplicationFactory(
            applicant=job_seeker,
            job=job,
            cover_letter="Test cover letter",
            resume="http://example.com/resume.pdf",
            status=Application.Status.PENDING,
        )

        assert application.applicant == job_seeker
        assert application.job == job
        assert application.cover_letter == "Test cover letter"
        assert application.resume == "http://example.com/resume.pdf"
        assert application.status == Application.Status.PENDING
        assert application.applied_at is not None
        assert str(application) == f"Application for {job.title} by {job_seeker.email}"

    def test_application_status_choices(self):
        job_seeker = JobSeekerUserFactory()
        job = JobFactory()
        application = ApplicationFactory(applicant=job_seeker, job=job)

        # Test valid status changes
        application.status = Application.Status.REVIEWED
        application.full_clean()
        application.save()
        assert application.status == Application.Status.REVIEWED

        application.status = Application.Status.SHORTLISTED
        application.full_clean()
        application.save()
        assert application.status == Application.Status.SHORTLISTED

        application.status = Application.Status.ACCEPTED
        application.full_clean()
        application.save()
        assert application.status == Application.Status.ACCEPTED

        application.status = Application.Status.REJECTED
        application.full_clean()
        application.save()
        assert application.status == Application.Status.REJECTED

        application.status = Application.Status.WITHDRAWN
        application.full_clean()
        application.save()
        assert application.status == Application.Status.WITHDRAWN

    def test_reviewed_at_update(self):
        job_seeker = JobSeekerUserFactory()
        job = JobFactory()
        application = ApplicationFactory(applicant=job_seeker, job=job, status=Application.Status.PENDING)
        assert application.reviewed_at is None

        application.status = Application.Status.REVIEWED
        application.save()
        assert application.reviewed_at is not None

        # reviewed_at should not change if status is updated again but not to a "reviewed" state
        old_reviewed_at = application.reviewed_at
        application.status = Application.Status.ACCEPTED
        application.save()
        assert application.reviewed_at == old_reviewed_at
