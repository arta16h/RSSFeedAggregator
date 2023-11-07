from celery import shared_task, Task
from celery.worker.request import Request
from celery.exceptions import Retry

from .models import Episode, Podcast
from .parser import Parser

MAX_CONCURRENCY = 3
MAX_RETRY = 3


class PodcastHandler(Request):
    def on_failure(self, info, send_failed=True, return_ok=False):
        # if type(info.exception) != Retry:
            # error_name = type(info.exception).__name__
            # podcast_id = self.kwargs["podcast_id"]
            # logger.critical(f'Failed to update podcast: id={podcast_id}: "{error_name}')
        return super().on_failure(
            info,
            send_failed=send_failed,
            return_ok=return_ok
        )
    
    def on_retry(self, exc_info):
        # error_name = type(exc_info.exception.exc).__name__
        # podcast_id = self.kwargs["podcast_id"]
        # logger.error(f'Failed to update podcast: "id={podcast_id}" "{error_name}"')
        return super().on_retry(exc_info)
    
    def on_success(self, **kwargs):
        # logger.info(kwargs)
        # logger.info("Successfully updated")
        return super().on_success(**kwargs)
    

class BaseTask(Task):
    Request = PodcastHandler
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = True
    retry_jitter = False


@shared_task(bind=True, base=BaseTask)
def reading_file(self, data):
    parser = Parser()
    try :
        parser.read_rss_file(data=data)
    except Exception as e:
        raise e


@shared_task(bind=True, base=BaseTask)
def parsing_rss(self, url):
    # message = f"trying to parse rss link"
    # logger.info(message)
    parser = Parser(url=url)

    try: 
        parser.rss_parser()
        # message = f"parsing rss link succeeded!"
        # logger.info(message)

    except Exception as e :
        # message = f"parsing rss link failed!" 
        # logger.error(message)
        raise e
    

@shared_task(bind=True, base=BaseTask)
def update(self, url):
    # message = f"trying to save podcast/episode to db"
    # logger.info(message)

    try: 
        podcast = Podcast.objects.get(url=url)
        a = podcast.episode_set.all().count()
        parser = Parser(url=url)
        parser.save_podcast_to_db(parser.rss_parser())
        b = podcast.episode_set.all().count()

        if b>a :
            pass

        # message = f"saving podcast/episode to db succeeded!"
        # logger.info(message)

    except Exception as e :
        # message = f"saving podcast/episode to db failed!" 
        # logger.error(message)
        raise e
