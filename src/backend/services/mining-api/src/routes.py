from src import app, socketio
from flask import request, jsonify
from .miningpool import MiningPool
import sys, os
import threading

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.exceptions import IncorrectPayloadException 
from shared.utils import BisonCoinUrls, send_post_request
from shared import HttpCode

COINBASE_AMOUNT = 10

blockchain_url = BisonCoinUrls.blockchain_url

# This is temporary till we move mining to user devices

difficulty = 4
def mine(transaction):
    # TODO actually mine

    # send transactions to blockchain
    response = send_post_request(blockchain_url.format("proof"), transaction)
   
    transactions.ready_to_mine()


def send_to_connected_clients(transaction):
    # ToDo
    print("To Be Sent to Miner", transaction)
    ongoing_proof_for_id = transaction["id"]
    socketio.emit("find_proof", transaction)

# transactions = MiningPool(sendToConnectedClients, True)
transactions = MiningPool(mine, True)

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
    

@socketio.on('echo')
def handle(message):
    socketio.emit("response", message)

@socketio.on('proof')
def handle_proofs(message):
    transactions.ready_to_mine()
    # TODO if proof for wrong id is received compare it with the current ongoing proof

    # TODO send the transaction to blockchain

    # TODO reward the miner (create a new transaction and send it to blockchain)

    socketio.emit("stop_finding", message)

@app.errorhandler(IncorrectPayloadException)
def handle_payload_error(e):
    return jsonify(error=e.json_message), e.return_code
