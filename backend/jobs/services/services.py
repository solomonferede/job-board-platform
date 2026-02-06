from datetime import timedelta

from django.utils import timezone

from ..models import Job


def deactivate_old_jobs(days=90):
    """
    Deactivate jobs older than `days`.
    """
    cutoff_date = timezone.now() - timedelta(days=days)
    old_jobs = Job.objects.filter(created_at__lt=cutoff_date, is_active=True)
    count = old_jobs.update(is_active=False)
    return count


def activate_job(job: Job):
    """
    Reactivate a job posting manually.
    """
    job.is_active = True
    job.save(update_fields=["is_active"])
    return job
