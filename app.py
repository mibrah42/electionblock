from flask import Flask, jsonify, request, redirect, url_for
from Blockchain import Blockchain
from broker import BlockchainBroker
import threading
import sys
from time import sleep

app = Flask(__name__)

blockchain = Blockchain()
broker = BlockchainBroker(blockchain)

@app.route("/")
def index():
    return jsonify(blockchain.getJSON())

# print(data['data'], file=sys.stdout)
@app.route('/api/vote', methods = ['POST'])
def vote():
    data = request.json
    blockchain.add_block(data['data'])
    broker.publish_chain()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)