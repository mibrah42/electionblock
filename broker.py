import zmq
import threading
from time import sleep
import json
from Blockchain import Blockchain
import random


TOPICS = {
    'PUBLISH_CHAIN': 'PUBLISH_CHAIN'
}

class BlockchainBroker:
    def __init__(self, blockchain):
        self.brokerBlockchain = blockchain 
        port = random.randint(3000, 6000)
        # Publisher setup
        context = zmq.Context()
        publisher_socket = context.socket(zmq.PUB)
        publisher_socket.bind('tcp://127.0.0.1:' + str(port))
        self.publisher = publisher_socket

        # Subscriber setup
        subscriber_socket = context.socket(zmq.SUB)
        subscriber_socket.connect('tcp://127.0.0.1:' + str(port))
        subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, TOPICS['PUBLISH_CHAIN'])
        self.subscriber = subscriber_socket
        thread = threading.Thread(target=self.subsribe_callback)
        thread.start()


    def subsribe_callback(self):
        while (True):
            message = self.subscriber.recv_string()
            chain = json.loads(message[len(TOPICS['PUBLISH_CHAIN']) + 1:])
            print(chain)

    def publish(self, topic, message):
        self.publisher.send_string(topic + " " + message)
    
    def publish_chain(self):
        self.publish(TOPICS['PUBLISH_CHAIN'], json.dumps(self.brokerBlockchain.getJSON()))


