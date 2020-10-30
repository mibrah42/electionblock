import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://127.0.0.1:2000')
socket.setsockopt_string(zmq.SUBSCRIBE, 'hello')

while (True):
    message = socket.recv_string()
    print(message)