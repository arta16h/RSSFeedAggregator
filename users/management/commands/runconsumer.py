import threading
from django.core.management.base import BaseCommand, CommandError

from ._pivate import run_activity_consumer

class Command(BaseCommand) :
    def handle(self, *args, **kwargs) :
        try:
            user_activity_threading = threading.Thread(target=run_activity_consumer)
            user_activity_threading.start()
            self.stdout.write(self.style.SUCCESS("Consuming started successfully... "))
        except Exception as e:
            raise CommandError(f"Consuming Failed! | {e}")