import pika

class Publisher:
    def __init__(self) :
        self.connection_parameter = pika.ConnectionParameters('localhost')


    def publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='signup-login')
        self.channel.basic_publish(exchange='', routing_key=queue, body='success' + message)
        print(f'{message} Published Successfully!')
        self.connection.close()

    def error_publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='signup-login')
        self.channel.basic_publish(exchange='', routing_key=queue, body='error!!' + message)
        print(f'{message} Published Successfully!')
        self.connection.close()