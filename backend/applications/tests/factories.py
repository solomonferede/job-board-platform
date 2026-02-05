import factory
from applications.models import Application
from jobs.tests.factories import JobFactory
from accounts.tests.factories import JobSeekerUserFactory


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Application

    applicant = factory.SubFactory(JobSeekerUserFactory)
    job = factory.SubFactory(JobFactory)
    cover_letter = factory.Faker("paragraph")
    resume = factory.django.FileField(filename="test_resume.pdf")
    status = Application.Status.APPLIED