from django.utils import timezone

from .models import Application


def withdraw_application(application):
    """
    Withdraw an application (Job seeker only).
    Allowed only if status is APPLIED.
    """
    if application.status != Application.Status.APPLIED:
        raise ValueError("Only applications in APPLIED state can be withdrawn.")

    application.status = Application.Status.WITHDRAWN
    application.withdrawn_at = timezone.now()
    application.save(update_fields=["status", "withdrawn_at"])
    return application


def update_application_status(application, status):
    """
    Update application status (Employer/Admin).
    """
    if application.status == Application.Status.WITHDRAWN:
        raise ValueError("Withdrawn applications cannot be updated.")

    application.status = status
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "reviewed_at"])
    return application
