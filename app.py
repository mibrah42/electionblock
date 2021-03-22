from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, Response
from flask_cors import CORS, cross_origin
from shard import Shard
from shard_broker import ShardBroker
import sys
import os
from time import sleep
import requests
import json
import uuid
import time
import pathlib
from file_manager import FileManager
from constants import BLOCK_VOTE_SIZE, SHARD_SIZE
import ast
from block import Block
from os import listdir
from os.path import isfile, join
from blockchain import Blockchain
import threading

# Configuring port and master api address.
DEFAULT_PORT = 5000
PORT = DEFAULT_PORT if len(sys.argv) < 2 else sys.argv[1]
MASTER_API_ADDRESS = "http://localhost:" + str(DEFAULT_PORT)
FOLDER_PATH = f"NODE_{PORT}"

# Setting up flask app instance.
app = Flask(__name__, static_folder=f'NODE_{PORT}')
cors = CORS(app)

# Initial setup for peers to join the network.
# Downloads files from the central server.


def initial_setup():
    # Download all shards from the server.
    try:
        response = requests.get(MASTER_API_ADDRESS + "/api/get_shards_length")
        if response.status_code == 200:
            data = response.content
            data = json.loads(data)
            if not pathlib.Path(FOLDER_PATH).exists():
                os.makedirs(FOLDER_PATH)
            for i in range(0, data['length']):
                response = requests.get(
                    f"{MASTER_API_ADDRESS}/NODE_{DEFAULT_PORT}/shard_{i}.db", allow_redirects=True)
                if response.status_code == 200:
                    with open(f"NODE_{PORT}/shard_{i}.db", 'wb') as f:
                        f.write(response.content)
    except:
        print("Main server is not running")


# Check if the current node is the central node or one of the peer nodes.
if PORT != DEFAULT_PORT:
    initial_setup()


# File manager for serializing and loading shards from the file system.
file_manager = FileManager(PORT)

# Blockchain instance for managing shards.
blockchain = Blockchain(file_manager)

# The current active shard instance. Defaults to 0 if system is blank.
active_shard = None

# Get the shard count from the file system. Defaults to 0.
shard_count = file_manager.get_shard_count()

if shard_count == 0:
    # Path doesn't exist, create new shard with genesis block.
    active_shard = Shard(0, Block.genesis_block(), True)
else:
    # Retrieve shard from file system.
    active_shard = file_manager.get_shard(shard_count - 1)

# Pub/Sub broker for publishing shards to peer nodes.
broker = ShardBroker(active_shard, file_manager)

# Endpoint for retrieving number of shards. Used by peer nodes to download initial set of files.


@app.route("/api/get_shards_length")
@cross_origin()
def shards_length():
    if pathlib.Path(FOLDER_PATH).exists():
        return jsonify({"length": len(listdir(FOLDER_PATH))}), 200
    else:
        return jsonify({"success": False}), 500

# Endpoint for retrieving specific shard from file system.


@app.route('/NODE_{PORT}/<path:filename>')
@cross_origin()
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join('.', f'NODE_{PORT}'), filename), 200


# Endpoint for retrieving votes per shard.
@app.route("/api/getvotes/<shard>")
@cross_origin()
def get_votes(shard):
    shard = int(shard)
    shard = file_manager.get_shard(shard)
    if shard is None:
        return jsonify({'success': False}), 500
    return jsonify(shard.get_json()), 200

# Endpoint for retrieving vote statistics (i.e. Votes per candidate, etc...).


@app.route("/api/getstats")
@cross_origin()
def stats():
    return jsonify(blockchain.get_stats()), 200


# Intermediary vote list for storing votes before commiting them to the blockchain. Once the vote_buffer has
# reached a length of BLOCK_VOTE_SIZE, we create a new block and commit it to the currently active shard.
vote_buffer = []

# Check if a voter has already voted for a particular campaign. Used to prevent duplicate votes.


def in_vote_buffer(campaign_id, voter_id):
    for vote in vote_buffer:
        if vote['voter_id'] == voter_id and vote['campaign_id'] == campaign_id:
            return True
    return False


# Endpoint for checking if a user has already voted.
@app.route('/api/hasvoted/<campaign_id>/<voter_id>')
@cross_origin()
def has_voted(campaign_id, voter_id):
    campaign = int(campaign_id)
    return jsonify({
        'has_voted': active_shard.has_voted(
            voter_id, campaign) or in_vote_buffer(campaign, voter_id)
    }), 200


# Endpoint for commiting a new vote. New votes are queued into the vote_buffer before being committed in batches.
@app.route('/api/vote', methods=['POST'])
@cross_origin()
def vote():
    global vote_buffer
    global active_shard
    global broker
    data = None
    if type(request.json) == dict:
        data = request.json
    else:
        data = json.loads(request.json)
    if not blockchain.has_voted(data['data']['voter_id'], data['data']['campaign_id']) and not in_vote_buffer(data['data']['campaign_id'], data['data']['voter_id']):
        vote_buffer.append(data['data'])
        if len(vote_buffer) >= BLOCK_VOTE_SIZE:
            # Create a new block once the vote_buffer has reached capacity.
            active_shard.add_block(vote_buffer)
            # Empty buffer.
            vote_buffer = []
            if active_shard.get_block_count() >= SHARD_SIZE:
                # Commit new shard to the file system once the SHARD_SIZE has been reached.
                old_shard_count = file_manager.get_shard_count()
                file_manager.serialize_shard(active_shard, old_shard_count)
                # Broadcast shard to subscribing peers.
                broker.publish_chain()
                # Increment shard count.
                shard_count = old_shard_count + 1
                # Load new shard as an active shard.
                active_shard = Shard(
                    shard_count, active_shard.shard[-1], False
                )
                # Load new broker with the new active shard.
                broker = ShardBroker(active_shard, file_manager)
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
