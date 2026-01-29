from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Job category or industry (e.g., IT, Marketing, Healthcare).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class JobType(models.Model):
    """
    Type of job (Full-time, Part-time, Contract, Internship).
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    Location for jobs (city, state, country). Can be extended with latitude/longitude later.
    """
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="Ethiopia")
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("city", "state", "country")  # avoid duplicate locations

    def __str__(self):
        parts = [self.city]
        if self.state:
            parts.append(self.state)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts)


class Job(models.Model):
    """
    Job posting.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs")
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, related_name="jobs")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="jobs")
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # newest jobs first

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.company}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company}"
