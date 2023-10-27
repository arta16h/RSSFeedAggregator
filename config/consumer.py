import pika

connection_parameter = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameter)
channel = connection.channel()
channel.queue_declare(queue='signup-login')

def log_user_activity(ch, method, property, body) :
    