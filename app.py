from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
from merkle_blockchain import MerkleBlockchain
from broker import BlockchainBroker
import threading
import sys
from time import sleep
import requests
import json
import uuid
import time
import random
import pathlib
from serialize_blockchain import BlockchainFileManager
from constants import BLOCKCHAIN_DB_FILE_NAME, BLOCK_VOTE_SIZE

app = Flask(__name__)
cors = CORS(app)

DEFAULT_PORT = 5000
PORT = DEFAULT_PORT if len(sys.argv) < 2 else sys.argv[1]
MASTER_API_ADDRESS = "http://localhost:" + str(DEFAULT_PORT)

BLOCKCHAIN_PATH = f"NODE_{PORT}/{BLOCKCHAIN_DB_FILE_NAME}"

file_manager = BlockchainFileManager(BLOCKCHAIN_PATH)

blockchain = None

if pathlib.Path(BLOCKCHAIN_PATH).exists():
    print("path exists")
    blockchain = file_manager.get_blockchain()
else:
    blockchain = MerkleBlockchain()

broker = BlockchainBroker(blockchain, file_manager)

# Only called by edge nodes (i.e. voting stations), not the centeral server.


def initial_setup():
    # New peers will ask the master node for a copy of the chain to start with.
    response = requests.get(MASTER_API_ADDRESS + "/api/getvotes")
    data = response.content
    data = json.loads(data)
    blockchain.replace_blockchain(data)


def simulate_voting():
    while True:
        sleep(0.5)
        vote = {
            'data': {
                'voter_id': str(uuid.uuid4()),
                'campaign_id': 1,
                'candidate_id': random.randint(1, 4),
                'timestamp': str(time.time())
            }
        }
        x = requests.post(f"{MASTER_API_ADDRESS}/api/vote",
                          json=json.dumps(vote))


if PORT != DEFAULT_PORT:
    initial_setup()
    simulate_voting()


@app.route("/api/getvotes")
@cross_origin()
def blocks():
    return jsonify(blockchain.get_json())


@app.route("/api/getstats")
@cross_origin()
def stats():
    return jsonify(blockchain.get_stats())


vote_buffer = []


def in_vote_buffer(vote_info):
    for vote in vote_buffer:
        if vote['voter_id'] == vote_info['voter_id'] and vote['campaign_id'] == vote_info['campaign_id']:
            return True
    return False


@app.route('/api/vote', methods=['POST'])
def vote():
    global vote_buffer
    data = None
    if type(request.json) == dict:
        data = request.json
    else:
        data = json.loads(request.json)
    if not blockchain.has_voted(data['data']['voter_id'], data['data']['campaign_id']) and not in_vote_buffer(data['data']):
        vote_buffer.append(data['data'])

        if len(vote_buffer) >= BLOCK_VOTE_SIZE:
            blockchain.add_block(vote_buffer)
            broker.publish_chain()
            vote_buffer = []
        print("VOTE_BUFFER", vote_buffer)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
