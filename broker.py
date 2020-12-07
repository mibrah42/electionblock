import threading
from time import sleep
import json
from Blockchain import Blockchain
import random
import redis
from serialize_blockchain import BlockchainFileManager

TOPICS = {
    'PUBLISH_CHAIN': 'PUBLISH_CHAIN'
}


class BlockchainBroker:
    def __init__(self, blockchain, file_manager):
        self.brokerBlockchain = blockchain
        self.file_manager = file_manager
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client = redis_client

        file_manager.serialize_blockchain(blockchain)
        subscriber = redis_client.pubsub()
        subscriber.subscribe(TOPICS['PUBLISH_CHAIN'])
        self.subscriber = subscriber

        thread = threading.Thread(target=self.subsribe_callback)
        thread.start()

    def subsribe_callback(self):
        for message in self.subscriber.listen():
            if type(message['data']) == bytes:
                updated_chain = self.brokerBlockchain.replace_blockchain(
                    json.loads(message['data'].decode('utf-8')))
                if updated_chain is not None:
                    self.file_manager.serialize_blockchain(updated_chain)

    def publish(self, topic, message):
        self.redis_client.publish(topic, message)

    def publish_chain(self):
        self.publish(TOPICS['PUBLISH_CHAIN'], json.dumps(
            self.brokerBlockchain.get_json()))


if __name__ == "__main__":
    blockchain = Blockchain()
    file_manager = BlockchainFileManager('blockchain_test.db')
    broker = BlockchainBroker(blockchain, file_manager)
    while(True):
        broker.redis_client.publish(TOPICS['PUBLISH_CHAIN'], "HELLO WORLD")
        sleep(1)
