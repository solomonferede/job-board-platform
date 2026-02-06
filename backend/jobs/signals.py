import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Job
from .services.cache import invalidate_job_cache

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Job)
def job_saved(sender, instance, **kwargs):
    invalidate_job_cache(job_id=instance.id)


@receiver(post_delete, sender=Job)
def job_deleted(sender, instance, **kwargs):
    invalidate_job_cache(job_id=instance.id)


@receiver(post_save, sender=Job)
def job_status_changed(sender, instance, created, **kwargs):
    logger.info(f"Signal fired for Job {instance.id}, active={instance.is_active}")
