from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application
from .tasks import send_application_confirmation


@receiver(post_save, sender=Application)
def application_created(sender, instance, created, **kwargs):
    if created:
        send_application_confirmation.delay(instance.id)
