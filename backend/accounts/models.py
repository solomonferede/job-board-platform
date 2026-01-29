from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        EMPLOYER = 'EMPLOYER', 'Employer'
        JOB_SEEKER = 'JOB_SEEKER', 'Job Seeker'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.JOB_SEEKER,
    )

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_employer(self):
        return self.role == self.Role.EMPLOYER

    def is_job_seeker(self):
        return self.role == self.Role.JOB_SEEKER