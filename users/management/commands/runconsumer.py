from django.core.management.base import BaseCommand, CommandError
from config.consumer_user import UserActivityConsumer

class Command(BaseCommand) :
    def handle(self, *args, **kwargs) :
        try:
            activity_consume = UserActivityConsumer()
            activity_consume.consume()
            self.stdout.write(self.style.SUCCESS("Consuming started successfully... "))
        except Exception as e:
            raise CommandError(f"Consuming Failed! | {e}")