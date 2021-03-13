from src import app, socketio
from flask import request, jsonify
from .miningpool import MiningPool
import sys, os
import threading
import json
from time import sleep
from hashlib import sha256
from flask_socketio import emit

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.exceptions import IncorrectPayloadException 
from shared.utils import BisonCoinUrls, send_post_request
from shared import HttpCode

blockchain_url = BisonCoinUrls.blockchain_url

ongoing_proof = None
ongoing_transaction = None
connected_clients = 0

# This is temporary till we move mining to user devices

difficulty = 4
def mine(transaction):
    # send transactions to blockchain
    response = send_post_request(blockchain_url.format("proof"), transaction)
   
    transactions.ready_to_mine()


def send_to_connected_clients(transaction):
    # ToDo
    global ongoing_proof, ongoing_transaction, connected_clients

    print("To Be Sent to Miner", transaction)
    ongoing_proof = transaction["id"]
    ongoing_transaction = transaction

    while (connected_clients == 0) : 
        sleep(0.5)

    socketio.emit("findProof", transaction)

transactions = MiningPool(send_to_connected_clients, True)
# transactions = MiningPool(mine, True)

@app.route("/")
def index():
    return "Hello From the Mining"

@app.route("/queue", methods= ["POST"])
def add_data_to_queue():
    data = request.get_json()
    
    if data is None:
        raise IncorrectPayloadException()
    
    transactions.add_to_pool(data)

    return jsonify(success=True), HttpCode.OK.value
    

def valid_proof(hash_, nonce):
    
    valid = (hash_.startswith('0' * difficulty))
    return valid and hash_ == sha256(
        (str(nonce) + ongoing_transaction["to"] + ongoing_transaction["from"] + str(ongoing_transaction["amount"]) + ongoing_transaction["id"] + ongoing_transaction["signature"]).encode('utf-8')
      ).hexdigest();

@socketio.on('connect')
def client_connect():
    global connected_clients
    connected_clients += 1
    print(connected_clients)

@socketio.on('disconnect')
def client_disconnect():
    global connected_clients
    connected_clients -= 1
    print(connected_clients)

@socketio.on('echo')
def handle(message):
    socketio.emit("response", message)

@socketio.on('proof')
def handle_proofs(message):
    global ongoing_proof, ongoing_transaction, COINBASE_AMOUNT, blockchain_url, blockchain_wallet_url, transactions
    
    if (ongoing_proof == message['id']):
        if valid_proof(message["proof"], message["nonce"]):

            # ignore the rest of the clients that try to send the proof
            ongoing_proof = None
            ongoing_transaction = None
            
            socketio.emit("stopProof", {})
            # new transactions are now ready to be mined    
            transactions.ready_to_mine()

            block_data = {}
            # send transactions to blockchain
            for key, value in message.items():
                block_data[key] = value
            
            for key, value in ongoing_transaction.items():
                block_data[key] = value
            
            send_post_request(blockchain_url.format("addBlock"), block_data)    
            emit('reward', {})

@app.errorhandler(IncorrectPayloadException)
def handle_payload_error(e):
    return jsonify(error=e.json_message), e.return_code
