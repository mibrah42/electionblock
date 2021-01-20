import threading
from time import sleep
import json
import random
import redis
from shard import Shard
from block import Block
from file_manager import FileManager

# Topics used in the Pub/Sub broker.
TOPICS = {
    'PUBLISH_CHAIN': 'PUBLISH_CHAIN'
}

class ShardBroker:
    def __init__(self, shard, file_manager):
        self.brokerShard = shard
        self.file_manager = file_manager

        # Configure redis client.
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client = redis_client

        # Configure redis Pub/Sub.
        subscriber = redis_client.pubsub()
        subscriber.subscribe(TOPICS['PUBLISH_CHAIN'])
        self.subscriber = subscriber

        # Run subscriber callback in background thread.
        thread = threading.Thread(target=self.subsribe_callback)
        thread.start()

    # Callback triggered on nodes when blockchain is published.
    def subsribe_callback(self):
        for message in self.subscriber.listen():
            if type(message['data']) == bytes:
                formatted = json.loads(message['data'].decode('utf-8'))
                # Validate shard and replace the current one with it if it's valid.
                updated_chain = self.brokerShard.replace_shard(
                    formatted
                )
                # If updated_chain returns a value, then the shard was successfully validated and thus we
                # can commit it to the file system.
                if updated_chain is not None:
                    self.file_manager.serialize_shard(
                        updated_chain, formatted['id']
                    )

    # Function triggered to broadcast shard to subscribing peers.
    def publish_chain(self):
        self.publish(TOPICS['PUBLISH_CHAIN'], json.dumps(
            self.brokerShard.get_json())
        )

    # Helper method for publishing message.
    def publish(self, topic, message):
        self.redis_client.publish(topic, message)


if __name__ == "__main__":
    shard = Shard(Block.genesis_block(), True)
    file_manager = FileManager('blockchain_test.db')
    broker = ShardBroker(shard, file_manager)
    while(True):
        broker.redis_client.publish(TOPICS['PUBLISH_CHAIN'], "HELLO WORLD")
        sleep(1)
