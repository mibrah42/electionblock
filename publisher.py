# import redis

# r = redis.Redis(host='localhost', port=6379, db=0)

# r.publish('topic', "hello world")

import zmq
from time import sleep 

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:5001')

messages = [100, 200, 300]
curMsg = 0

while (True):
    sleep(1)
    socket.send_string("REPLACE_CHAIN {curMsg: messages[curMsg]}")
    if (curMsg == 2):
        curMsg = 0
    else:
        curMsg = curMsg + 1