import logging
from celery import shared_task, Task
from celery.worker.request import Request
from celery.exceptions import Retry
from .models import Podcast


logger = logging.getLogger('celery-logger')

MAX_CONCURRENCY = 3
MAX_RETRY = 3


class PodcastHandler(Request):
    def on_failure(self, info, send_failed=True, return_ok=False):
        if type(info.exception) != Retry:
            error_name = type(info.exception).__name__
            podcast_id = self.kwargs["podcast_id"]
            logger.critical(f'Failed to update podcast: id={podcast_id}: "{error_name}')
        return super().on_failure(
            info,
            send_failed=send_failed,
            return_ok=return_ok
        )
    
    def on_retry(self, exc_info):
        error_name = type(exc_info.exception.exc).__name__
        podcast_id = self.kwargs["podcast_id"]
        logger.error(f'Failed to update podcast: "id={podcast_id}" "{error_name}"')
        return super().on_retry(exc_info)
    
    def on_success(self, **kwargs):
        logger.info(kwargs)
        logger.info("Successfully updated")
        return super().on_success(**kwargs)
    

class BaseTask(Task):
    Request = PodcastHandler
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = True
    retry_jitter = False