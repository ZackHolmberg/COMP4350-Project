"""routes fo the mining api"""
import sys
import os
from time import sleep
from hashlib import sha256
from flask_socketio import emit
from flask import request, jsonify
from src import app, socketio
from .miningpool import MiningPool

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.exceptions import IncorrectPayloadException
from shared.utils import BisonCoinUrls, send_post_request
from shared import HttpCode

BLOCKCHAIN_URL = BisonCoinUrls.blockchain_url

ongoing_proof = None
ongoing_transaction = None
connected_clients = 0

difficulty = 4


def send_to_connected_clients(transaction):
    """
        A method supplied to the mining pool for sending the current
        transaction that is ready to be mined to a list of connected
        miners.

        params:
            transaction: The transaction that is to be mined.

        Returns:
            N/A
    """
    global ongoing_proof, ongoing_transaction, connected_clients

    ongoing_proof = transaction["id"]
    ongoing_transaction = transaction

    while connected_clients == 0:
        sleep(0.5)

    socketio.emit("findProof", transaction)


transactions = MiningPool(send_to_connected_clients, True)


@app.route("/")
def index():
    """
        A route that returns a greeting if the service is up

        params:
            N/A

        Returns:
            a greeting string
    """
    return "Hello From the Mining"


@app.route("/queue", methods=["POST"])
def add_data_to_queue():
    """
        A route that adds a transaction to the queue of transactions
        waiting to be mined.

        params:
            data: the transaction that is to be added to the queue.

        Returns:
            a json string with the following:
                success: True if the transaction was successfully added
                         the queue, else false
        """
    data = request.get_json()

    if data is None:
        raise IncorrectPayloadException()

    transactions.add_to_pool(data)

    return jsonify(success=True), HttpCode.OK.value


def valid_proof(hash_, nonce) -> bool:
    """
        A method to check if a received proof is correct or not.

        params:
            hash_: the received hash value
            nonce: the received nonce value

        Returns:
            True if the transaction is valid, else false
    """
    valid = (hash_.startswith('0' * difficulty))
    to_hash = (str(nonce) + str(
        ongoing_transaction["amount"]) + str(
        ongoing_transaction["timestamp"]) + ongoing_transaction["id"] +\
            ongoing_transaction["signature"])
    to_hash = to_hash.replace("\n", "")
    to_hash = to_hash.replace("\r", "")
    computed_hash = sha256(to_hash.encode('utf-8')).hexdigest()
    return valid and hash_ == computed_hash


@socketio.on('connect')
def client_connect():
    """
        A method that increments the number of connected clients
        when a new miner connects.

        params:
            N/A

        Returns:
            N/A
    """
    global connected_clients
    connected_clients += 1


@socketio.on('disconnect')
def client_disconnect():
    """
        A method that decrements the number of connected clients
        when a miner disconnects.

        params:
            N/A

        Returns:
            N/A
    """
    global connected_clients
    connected_clients -= 1


@socketio.on('echo')
def handle(message):
    """
        A method that emits the received message back to the client.

        params:
            message: the message received from the client.

        Returns:
            N/A
    """
    socketio.emit("response", message)


@socketio.on('proof')
def handle_proofs(message):
    """
        A method to handle porrfs received from the miners.
        if a valid proof is received, the ongoing proof is set to None,
        and the clients are told to stop mining for a proof. The state is
        set to be ready to be mind and The new transaction block is
        then added to the blockchain, appropriate rewarding subroutine is also
        executed.

        params:
            message: a message containing the proof and nonce

        Returns:
            N/A
    """
    global ongoing_proof, ongoing_transaction, BLOCKCHAIN_URL, transactions

    if ongoing_proof == message['id']:
        if valid_proof(message["proof"], message["nonce"]):
            # ignore the rest of the clients that try to send the proof
            ongoing_proof = None
            socketio.emit("stopProof", None)
            # new transactions are now ready to be mined
            block_data = {}
            # send transactions to blockchain
            for key, value in message.items():
                block_data[key] = value

            for key, value in ongoing_transaction.items():
                block_data[key] = value

            ongoing_transaction = None
            transactions.ready_to_mine()

            send_post_request(BLOCKCHAIN_URL.format("addBlock"), block_data)
            emit('reward', None)


@app.errorhandler(IncorrectPayloadException)
def handle_payload_error(error):
    """
        A method to handle the incorrect payload exception

        params:
            error: the error received

        Returns:
            The error return code and json string containing the following:
                error: the error message as json
    """
    return jsonify(error=error.json_message), error.return_code
