from celery import shared_task
from django.core.mail import send_mail

from .models import User


@shared_task
def send_welcome_email(user_id):
    user = User.objects.get(id=user_id)

    send_mail(
        subject="Welcome to Job Board",
        message=f"Hi {user.first_name}, welcome to Job Board!",
        from_email="noreply@jobboard.com",
        recipient_list=[user.email],
        fail_silently=True,
    )
