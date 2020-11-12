class Controller:
    def __init__(self):
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client = redis_client

        thread = threading.Thread(target=self.subsribe_callback)
        thread.start()

    def subsribe_callback(self):
        for message in self.subscriber.listen():
            print(message)
    
    def publish(self, topic, message):
        self.redis_client.publish(topic, message)
    
    def move(self, table_number):
        self.publish("MOVE_ROBOT", table_number)
