import pika
import logging

connection_parameter = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameter)
channel = connection.channel()
channel.queue_declare(queue='signup-login')

logger = logging.getLogger('user_actions')

def log_user_activity(channel, method, property, body) :
    body = body.decode("utf-8")
    if body.startswith('success') :    
        logger.info(body.lstrip("success"))
        print(body)
    elif body.startswith('error!!') :
        logger.error(body.lstrip("error!!"))
        print("2")
    else :
        print(body)

channel.basic_consume(queue='signup-login', on_message_callback=log_user_activity, auto_ack=True)
print('Start Consuming...')
channel.start_consuming()