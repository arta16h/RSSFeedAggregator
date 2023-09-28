from celery import shared_task, Task
from .models import Comment


class BaseTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = True
    retry_jitter = False
    task_acks_late = True
    task_concurrency = 4
    worker_prefetch_multiplier = 1

