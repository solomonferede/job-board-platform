import pytest
from jobs.models import Category, JobType, Location, Company, Job
from jobs.tests.factories import (
    CategoryFactory,
    JobTypeFactory,
    LocationFactory,
    CompanyFactory,
    JobFactory,
)
from accounts.tests.factories import EmployerUserFactory


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        category = CategoryFactory(name="Engineering")
        assert category.name == "Engineering"
        assert str(category) == "Engineering"

    def test_category_unique_name(self):
        CategoryFactory(name="Engineering")
        with pytest.raises(Exception):  # IntegrityError or ValidationError
            CategoryFactory(name="Engineering")


@pytest.mark.django_db
class TestJobTypeModel:
    def test_create_job_type(self):
        job_type = JobTypeFactory(name="Full-time")
        assert job_type.name == "Full-time"
        assert str(job_type) == "Full-time"

    def test_job_type_unique_name(self):
        JobTypeFactory(name="Full-time")
        with pytest.raises(Exception):
            JobTypeFactory(name="Full-time")


@pytest.mark.django_db
class TestLocationModel:
    def test_create_location(self):
        location = LocationFactory(name="Remote")
        assert location.name == "Remote"
        assert str(location) == "Remote"

    def test_location_unique_name(self):
        LocationFactory(name="Remote")
        with pytest.raises(Exception):
            LocationFactory(name="Remote")


@pytest.mark.django_db
class TestCompanyModel:
    def test_create_company(self):
        employer = EmployerUserFactory()
        company = CompanyFactory(name="Tech Corp", created_by=employer)
        assert company.name == "Tech Corp"
        assert company.created_by == employer
        assert str(company) == "Tech Corp"

    def test_company_description_and_website(self):
        company = CompanyFactory(description="Leading tech company", website="http://tech.com")
        assert company.description == "Leading tech company"
        assert company.website == "http://tech.com"


@pytest.mark.django_db
class TestJobModel:
    def test_create_job(self):
        employer = EmployerUserFactory()
        company = CompanyFactory(created_by=employer)
        category = CategoryFactory()
        job_type = JobTypeFactory()
        location = LocationFactory()

        job = JobFactory(
            title="Software Engineer",
            created_by=employer,
            company=company,
            category=category,
            job_type=job_type,
            location=location,
            salary=120000,
            is_active=True,
        )

        assert job.title == "Software Engineer"
        assert job.created_by == employer
        assert job.company == company
        assert job.category == category
        assert job.job_type == job_type
        assert job.location == location
        assert job.salary == 120000
        assert job.is_active is True
        assert str(job) == "Software Engineer at Tech Corp" # Assuming CompanyFactory creates a company with "Tech Corp"

    def test_job_skills(self):
        job = JobFactory(skills=["Python", "Django"])
        assert job.skills.count() == 2
        assert "Python" in [s.name for s in job.skills.all()]
        assert "Django" in [s.name for s in job.skills.all()]

    def test_job_default_active_status(self):
        job = JobFactory()
        assert job.is_active is True
