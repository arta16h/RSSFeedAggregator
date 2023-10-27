import pika

class Publisher:
    def __init__(self) :
        self.connection_parameter = pika.ConnectionParameters('localhost')
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare('signup-login')

    def publish(self, message, queue) :
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)
        print(f'{message} Published Successfully!')