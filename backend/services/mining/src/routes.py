from src import app, socketio
from flask import request, jsonify
from .MiningPool import MiningPool
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode, FailureReturnString


def sendToConnectedClients(transaction):
    # ToDo
    print("To Be Sent to Miner", transaction)

transactions = MiningPool(sendToConnectedClients)

@app.route("/")
def index():
    return "Hello From the Mining"


@app.route("/queue", methods= ["POST"])
def addDataToQueue():
    data = request.get_json()

    if data is None:
        return jsonify(FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST
    
    transactions.addToPool(data)

    return jsonify(success=True), HttpCode.OK
    

@socketio.on('echo')
def handle(message):
    socketio.emit("response", message, callback=msg)

def msg(methods=['GET', 'POST']):
    print('message was received!!!')

