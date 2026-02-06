from celery import shared_task
from django.core.mail import send_mail

from .models import Application


@shared_task
def send_application_confirmation(application_id):
    application = Application.objects.select_related("job", "applicant").get(
        id=application_id
    )

    send_mail(
        subject=f"Application submitted for {application.job.title}",
        message=(
            f"Hi {application.applicant.first_name},\n\n"
            f"You successfully applied for '{application.job.title}'."
        ),
        from_email="noreply@jobboard.com",
        recipient_list=[application.applicant.email],
        fail_silently=True,
    )
