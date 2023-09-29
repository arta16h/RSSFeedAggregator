import logging
from celery import shared_task
from .models import Podcast


logger = logging.getLogger('celery-logger')

MAX_CONCURRENCY = 3
MAX_RETRY = 3