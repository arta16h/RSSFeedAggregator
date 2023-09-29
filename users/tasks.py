import logging
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse_lazy


logger = logging.getLogger("celery-logger")


@shared_task
def send_reset_password_email(receiver, code):
    subject = "RSS-Feed password reset"
    reset_password_link = reverse_lazy("reset_password", kwargs={"code":code})
    link = f"{settings.BASE_URL}{reset_password_link}"
    message = (
        f"Click the link below in order to reset your password\n"
        f"{link}"
    )
    recipient_list = [receiver]
    email = EmailMessage(subject=subject, body=message, to=recipient_list)
    email.send()
    logger.info(f'password reset link sent to "{receiver}" "code={code}"')