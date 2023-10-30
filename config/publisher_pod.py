import pika

class Publisher:
    def __init__(self) :
        self.connection_parameter = pika.ConnectionParameters('localhost')

    def publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='podcast-update')
        a = self.channel.basic_publish(exchange='', routing_key=queue, body=message)
        print(a)
        print(f'{message} Published Successfully!')
        self.connection.close()

    def error_publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='podcast-update')
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)
        print(f'{message} Published Successfully!')
        self.connection.close()

publishh = Publisher()
publishh.publish("hi!", "podcast-update")