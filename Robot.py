import threading
import redis

class Robot:
    def __init__():
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client = redis_client

        subscriber = redis_client.pubsub()
        subscriber.subscribe("MOVE_ROBOT")
        self.subscriber = subscriber

        thread = threading.Thread(target=self.subsribe_callback)
        thread.start()

        def subsribe_callback(self):
            for message in self.subscriber.listen():
                print("Table number:", message)
        
        def publish(self, topic, message):
            self.redis_client.publish(topic, message)

