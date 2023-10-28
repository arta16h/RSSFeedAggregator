import pika
import logging

connection_parameter = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameter)
channel = connection.channel()
channel.queue_declare(queue='signup-login')

logger = logging.getLogger('user_actions')

def log_user_activity(channel, method, property, body) :
    if body[:8] == 'success' :    
        logger.info(body[7:])
        print(":D")
    elif body[:8] == 'error!!' :
        logger.error(body[7:])
        print(":|")

channel.basic_consume(queue='signup-login', on_message_callback=log_user_activity, auto_ack=True)
print('Start Consuming...')
channel.start_consuming()