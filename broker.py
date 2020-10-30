import zmq
import threading
from time import sleep
import json
from Blockchain import Blockchain
import random
import redis

TOPICS = {
    'PUBLISH_CHAIN': 'PUBLISH_CHAIN'
}

class BlockchainBroker:
    def __init__(self, blockchain):
        self.brokerBlockchain = blockchain

        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client = redis_client

        subscriber = redis_client.pubsub()
        subscriber.subscribe(TOPICS['PUBLISH_CHAIN'])
        self.subscriber = subscriber

        thread = threading.Thread(target=self.subsribe_callback)
        thread.start()

    def subsribe_callback(self):
        for message in self.subscriber.listen():
            if type(message['data']) == bytes:
                self.brokerBlockchain.replace_blockchain(json.loads(message['data'].decode('utf-8')))

    def publish(self, topic, message):
        self.redis_client.publish(topic, message)
    
    def publish_chain(self):
        self.publish(TOPICS['PUBLISH_CHAIN'], json.dumps(self.brokerBlockchain.getJSON()))


if __name__ == "__main__":
    blockchain = Blockchain()
    broker = BlockchainBroker(blockchain)
    while(True):
        broker.redis_client.publish(TOPICS['PUBLISH_CHAIN'], "HELLO WORLD")
        sleep(1)