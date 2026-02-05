import factory
from jobs.models import Category, JobType, Location, Company, Job
from accounts.tests.factories import EmployerUserFactory, JobSeekerUserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class JobTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobType

    name = factory.Sequence(lambda n: f"Job Type {n}")


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Sequence(lambda n: f"Location {n}")


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Sequence(lambda n: f"Company {n}")
    description = factory.Faker("paragraph")
    website = factory.Faker("url")
    created_by = factory.SubFactory(EmployerUserFactory)


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    title = factory.Faker("job")
    description = factory.Faker("text")
    requirements = factory.Faker("text")
    salary = factory.Faker("random_int", min=30000, max=150000)
    is_active = True
    created_by = factory.SubFactory(EmployerUserFactory)
    company = factory.SubFactory(CompanyFactory, created_by=factory.SelfAttribute('..created_by'))
    category = factory.SubFactory(CategoryFactory)
    job_type = factory.SubFactory(JobTypeFactory)
    location = factory.SubFactory(LocationFactory)

    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for skill in extracted:
                self.skills.add(skill)
