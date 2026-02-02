from django.utils import timezone
from .models import Application


def withdraw_application(application):
    if application.status != Application.Status.APPLIED:
        raise ValueError("Only applications in APPLIED state can be withdrawn.")

    application.status = Application.Status.WITHDRAWN
    application.withdrawn_at = timezone.now()
    application.save()
    return application


def update_application_status(application, status):
    application.status = status
    application.reviewed_at = timezone.now()
    application.save()
    return application
