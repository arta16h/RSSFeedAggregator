from celery import shared_task, Task
from django.core.mail import send_mail

from .models import Comment, Subscribe
from podcasts.models import Podcast

class BaseTask(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    task_time_limit=120
    retry_backoff = True
    retry_jitter = False

@shared_task(bind=True, base=BaseTask)
def create_comment(self, content, episode_id, user_id):
    Comment.objects.create(content=content, object_id=episode_id, user_id=user_id)
    return f"New comment submitted by {user_id}"


@shared_task(bind=True, base=BaseTask)
def notify_users(podcast_id) :
    subscriber_info = Subscribe.objects.filter(podcast__id = podcast_id).values_list("user__email", "user__username")
    podcast = Podcast.objects.get(id=podcast_id)

    for email, username in subscriber_info :
        message = f"Dear {username}, {podcast.title} has new episodes :D"
        send_notify_email.delay(email, message)


@shared_task(bind=True, base=BaseTask)
def send_notify_email(email, message) :
    send_mail(subject="New Episodes :D", message=message, recipient_list=[email])