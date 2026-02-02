from celery import shared_task


@shared_task
def notify_employer_new_application(application_id):
    # send email / notification
    pass


@shared_task
def notify_applicant_status_change(application_id):
    # send email / notification
    pass
