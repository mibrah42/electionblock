from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
from Blockchain import Blockchain
from broker import BlockchainBroker
import threading
import sys
from time import sleep
import requests
import json

app = Flask(__name__)
cors = CORS(app)

blockchain = Blockchain()
broker = BlockchainBroker(blockchain)

DEFAULT_PORT = 5000
PORT = DEFAULT_PORT if len(sys.argv) < 2 else sys.argv[1]
MASTER_API_ADDRESS = "http://localhost:" + str(DEFAULT_PORT)

def initial_setup():
    # New peers will ask the master node for a copy of the chain to start with.
    response = requests.get(MASTER_API_ADDRESS + "/api/getvotes")
    data = response.content
    data = json.loads(data)
    blockchain.replace_blockchain(data)

if PORT != DEFAULT_PORT:
    initial_setup()

@app.route("/api/getvotes")
@cross_origin()
def index():
    return jsonify(blockchain.getJSON())

vote_buffer = []

# print(data['data'], file=sys.stdout)
@app.route('/api/vote', methods = ['POST'])
def vote():
    data = request.json
    blockchain.add_block(data['data'])
    broker.publish_chain()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=PORT)