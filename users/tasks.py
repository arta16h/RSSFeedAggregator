from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_reset_password_email(receiver, code):
    send_mail(subject="RSS-Feed Password Reset", message=f"Enter this code to reset your password : {code}", recipient_list=[receiver])