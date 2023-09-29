from celery import shared_task, Task
from .models import Comment


class BaseTask(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = True
    retry_jitter = False

