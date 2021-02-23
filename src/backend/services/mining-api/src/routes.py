from src import app, socketio
from flask import request, jsonify
from .MiningPool import MiningPool
import sys, os
import threading

sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode, FailureReturnString

def sendToConnectedClients(transaction):
    # ToDo
    socketio.emit("find_proof", transaction)

transactions = MiningPool(sendToConnectedClients, True)

@app.route("/")
def index():
    return "Hello From the Mining"

@app.route("/queue", methods= ["POST"])
def queue_transaction():
    data = request.get_json()

    if data is None:
        return jsonify(FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST
    
    transactions.addToPool(data)

    return jsonify(success=True), HttpCode.OK
    

@socketio.on('echo')
def handle(message):
    socketio.emit("response", message, callback=msg)

@socketio.on('proof')
def handle_proofs(message):
    transactions.ready_to_mine()
    # TODO send the transaction to blockchain

    # TODO reward the miner

    # broadcast to the clients that a proof was found 
    socketio.emit("stop_finding", message)
