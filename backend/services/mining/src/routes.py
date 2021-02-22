from src import app, socketio
from flask import request, jsonify
from .MiningPool import MiningPool
import sys, os
import threading

sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode, FailureReturnString

send = threading.Condition()
ready_to_mine = False

def sendToConnectedClients(transaction):
    # ToDo
    print("To Be Sent to Miner", transaction)

    with send:
        while not ready_to_mine:
            send.wait()

        socketio.emit("find_proof", transaction)

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

@socketio.on('proof')
def handle(message):
    with send:
        ready_to_mine = True
        send.notify_all()
    # socketio.emit("response", message, callback=msg)

def msg(methods=['GET', 'POST']):
    print('message was received!!!')

