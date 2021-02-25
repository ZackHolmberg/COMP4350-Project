from src import app, socketio
from flask import request, jsonify
from .MiningPool import MiningPool
import sys, os
import threading
import requests

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString


COINBASE_AMOUNT = 10

# This is temporary till we move mining to user devices

difficulty = 4
def mine(transaction):
    # TODO actually mine

    # send transactions to blockchain

   
    response = requests.post(
            "http://blockchain:5000/proof", json=transaction)
    
   
    transactions.ready_to_mine()


def sendToConnectedClients(transaction):
    # ToDo
    print("To Be Sent to Miner", transaction)
    try:
        ongoing_proof_for_id = transaction["id"]
        socketio.emit("find_proof", transaction)
    except Exception as e:
        print(e)

# transactions = MiningPool(sendToConnectedClients, True)
transactions = MiningPool(mine, True)

@app.route("/")
def index():
    return "Hello From the Mining"

@app.route("/queue", methods= ["POST"])
def addDataToQueue():
    data = request.get_json()

    if data is None:
        return jsonify(FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST.value
    
    transactions.addToPool(data)

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

    # TODO send receivers the message to stop finding the proof
    socketio.emit("stop_finding", message)
