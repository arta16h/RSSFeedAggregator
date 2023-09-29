from celery import shared_task, Task
from .models import Comment, Episode


class BaseTask(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = True
    retry_jitter = False

@shared_task(base=BaseTask, task_time_limit=120)
def create_comment(content, episode_id, user_id):
    Comment.objects.create(content=content, object_id=episode_id, user_id=user_id)
    return f"New comment submitted by {user_id}"