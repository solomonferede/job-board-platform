import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True


class JobSeekerUserFactory(UserFactory):
    role = User.Role.JOB_SEEKER


class EmployerUserFactory(UserFactory):
    role = User.Role.EMPLOYER


class AdminUserFactory(UserFactory):
    role = User.Role.ADMIN
    is_staff = True
    is_superuser = True
