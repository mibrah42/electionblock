import pika
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
import sys

app = Flask(__name__)
cors = CORS(app)

DEFAULT_PORT = 6002
PORT = DEFAULT_PORT if len(sys.argv) < 2 else sys.argv[1]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='vote_queue')


@app.route('/api/vote', methods=['POST'])
@cross_origin()
def vote():
    print(str(request.json))
    channel.basic_publish(
        exchange='',
        routing_key='vote_queue',
        body=str(request.json),
    )
    return jsonify({
        'success': True
    })


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
