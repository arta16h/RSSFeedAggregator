from celery import shared_task, Task
from celery.worker.request import Request
from celery.exceptions import Retry

from .models import Podcast
from .parser import Parser
from config.publisher import Publisher
from interactions.tasks import notify_users

MAX_CONCURRENCY = 3
MAX_RETRY = 3

publisher = Publisher()

class PodcastHandler(Request):
    def on_failure(self, info, send_failed_event=True, return_ok=False):
        if type(info.exception) != Retry:
            error = type(info.exception).__name__
            publisher.error_publish(f"Failed to update podcast due to {error}", queue='podcast-update')
        return super().on_failure(
            info,
            send_failed_event=send_failed_event,
            return_ok=return_ok
        )
    
    def on_retry(self, exc_info):
        error = type(exc_info.exception.exc).__name__
        publisher.error_publish(f"Failed to update podcast due to {error}", queue='podcast-update')
        return super().on_retry(exc_info)
    
    def on_success(self, **kwargs):
        publisher.publish("Successfully updated", queue='podcast-update')
        return super().on_success(**kwargs)
    

class BaseTask(Task):
    Request = PodcastHandler
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = True
    retry_jitter = False


# @shared_task(bind=True, base=BaseTask)
# def reading_file(self, data):
#     parser = Parser()
#     try :
#         parser.read_rss_file(data=data)
#     except Exception as e:
#         raise e

@shared_task(bind=True, base=BaseTask)
def parsing_rss(self, url):
    publisher.publish("Trying to parse RSS url...", queue='podcast-update')
    parser = Parser(url=url)

    try: 
        parser.rss_parser()
        publisher.publish("Parsing Succeeded", queue='podcast-update')

    except Exception as e :
        publisher.error_publish("Parsing Failed!", queue='podcast-update')
        raise e
    

@shared_task(bind=True, base=BaseTask)
def update_single_podcast(self, url):
    publisher.publish("Trying to Save Podcast/Episode to DB...", queue='podcast-update')

    try: 
        podcast = Podcast.objects.get(url=url)
        a = podcast.episode_set.all().count()
        parser = Parser(url=url)
        parser.save_podcast_to_db(parser.rss_parser())
        b = podcast.episode_set.all().count()

        if b > a :
            notify_users.delay(podcast.id)
        publisher.publish("Saving to Db Succeeded", queue='podcast-update')

    except Exception as e :
        publisher.error_publish("Saving to DB Failed!", queue='podcast-update')
        raise e
    

@shared_task(bind=True, base=BaseTask)
def update_all_podcasts(self) :
    publisher.publish("Trying to Update all Podcasts...", queue='podcast-update')
    
    try:
        podcast_urls = Podcast.objects.all().values_list("websiteUrl")
        for url in podcast_urls :
            update_single_podcast.delay(url[0])
        publisher.publish("Saving all Podcasts to DB Succeeded", queue='podcast-update')

    except Exception as e :
        publisher.error_publish("Saving all Podcasts to DB Failed!", queue='podcast-update')
        raise e
    
@shared_task(bind=True, base=BaseTask)
def save_single_podcast(self, url):
    publisher.publish("Trying to Save Podcast/Episode to DB...", queue='podcast-update')

    try: 
        parser = Parser(url=url)
        parser.save_podcast_to_db(parser.rss_parser())
        publisher.publish("Saving to Db Succeeded", queue='podcast-update')

    except Exception as e :
        publisher.error_publish("Saving to DB Failed!", queue='podcast-update')
        raise e