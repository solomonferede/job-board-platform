from django.db import models
from django.conf import settings
from jobs.models import Job


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        REVIEWED = "REVIEWED", "Reviewed"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    cover_letter = models.TextField()
    resume = models.FileField(upload_to="resumes/")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    reviewed_at = models.DateTimeField(null=True, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("applicant", "job")
        indexes = [
            models.Index(fields=["job"]),
            models.Index(fields=["applicant"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.applicant} → {self.job}"
