import pika
import logging
from django.conf import settings

class UserActivityConsumer :
    def __init__(self) -> None:
        self.logger = logging.getLogger('user_actions')
        self.connection_parameter = pika.ConnectionParameters(settings.RABBITMQ_HOST)
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='signup-login')


    def consume(self):
        self.channel.basic_consume(queue='signup-login', on_message_callback=self.log_user_activity, auto_ack=True)
        print('Start Consuming...')
        self.channel.start_consuming()

    def log_user_activity(self, channel, method, property, body) :
        body = body.decode("utf-8")
        if body.startswith('Success : ') :    
            self.logger.info(body.lstrip("Success : "))
            print(body)
        elif body.startswith('Error : ') :
            self.logger.error(body.lstrip("Error : "))
            print(body)
        else :
            print("Error!")

