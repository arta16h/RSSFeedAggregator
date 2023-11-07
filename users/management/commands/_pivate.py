from config.consumer_user import UserActivityConsumer

def run_activity_consumer() :
    activity_consume = UserActivityConsumer()
    activity_consume.consume()