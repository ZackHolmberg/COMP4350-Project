"""module containing the routes for the blockchain api"""
import sys
import os
from flask import request, jsonify
from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import blockchain, Blockchain
from .exceptions import WalletException


sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared.exceptions import IncorrectPayloadException
from shared import HttpCode

@app.route("/")
def index():
    """
    endpoint to test if the service is running

            Parameters:
                    None

            Returns:
                    greeting message if the service is up
    """
    return "Hello Blockchain"


@app.route('/chain', methods=['GET'])
def get_chain():
    """
    Endpoint to get the entire blockchain

            Parameters: through request:
                    N/A

            Returns:
                    A status code and json string containing the following
                        length (int): the length of the chain
                        chain (list of json strings): The blockchain
    """
    chain = []
    for block in blockchain.chain:
        chain.append(block.toJSON())
    return jsonify(length=len(chain), chain=chain), HttpCode.OK.value


@app.route('/addBlock', methods=['POST'])
def proof():
    """
    Endpoint to add a new block to the blockchain created from the supplied transaction

            Parameters: from request:
                    json data containing the following details about the transaction:
                        from (string): the sender address
                        to (string): the receiver address
                        amount (float): the amount to be sent
                        timestamp (float): the unix timestamp of the transaction
                        id (string): the id of the transaction
                        signature (string): the sender's signature on the transaction

            Returns:
                    Success = True on success else error
    """
    data = request.get_json()
    try:
        new_transaction = Transaction(
            data["from"],
            data["to"],
            data["amount"],
            data["timestamp"],
            data["id"],
            data["signature"]
        )
        miner_id = data["minerId"].upper()
        proof = data["proof"]
        nonce = data["nonce"]

    except KeyError as error:
        raise IncorrectPayloadException() from error

    new_block = Block(
        len(blockchain.chain),
        new_transaction,
        nonce,
        proof,
        blockchain.get_last_block().hash,
        miner_id,
        Blockchain.COINBASE_AMOUNT
    )

    # We guarantee that all the necessary validation has been done by this point, so simply add the
    # new block to the chain
    blockchain.chain.append(new_block)

    blockchain.add_to_wallet(miner_id, Blockchain.COINBASE_AMOUNT)

    return jsonify(success=True), HttpCode.CREATED.value


@app.route('/wallet/checkWallet', methods=['POST'])
def check_wallet_exists():
    """
    endpoint to test if the service is running, returns a welcome string and status=True

            Parameters: from request:

                    umnetId (string): the umnetId to be searched for.

            Returns:
                    status code and json string containing:
                        valid = true or false

                    -or-

                    error message
    """
    try:
        data = request.get_json()
        wallet_id = data["umnetId"].upper()
        exists = wallet_id in blockchain.wallets
        return jsonify(valid=exists), HttpCode.OK.value

    except KeyError as error:
        raise IncorrectPayloadException() from error


@app.route('/wallet/addWallet', methods=['POST'])
def add_wallet():
    """
    endpoint to add a new wallet

            Parameters: from request:
                    umnetId (string): the umnetId to be searched for

            Returns:
                    status code and json data containing:
                        success (boolean) : true on success else false

                        -or-

                        error message
    """

    try:
        data = request.get_json()
        wallet_id = data["umnetId"].upper()
        success = blockchain.add_wallet(wallet_id)
        return jsonify(success=success), HttpCode.CREATED.value

    except KeyError as error:
        raise IncorrectPayloadException() from error


@app.route('/wallet/createTransaction', methods=['POST'])
def create_transaction():
    """
    endpoint to add a new wallet

            Parameters: from request:

                    umnetId (string): the umnetId to be searched for

            Returns:

                    status code and json data containing:
                        success (boolean) : true on success else false

                        -or-

                        error message
    """
    try:
        data = request.get_json()
        wallet_id = data["from"].upper()
        amount = data["amount"]
        receiver = data["to"].upper()

    except KeyError as error:
        raise IncorrectPayloadException() from error

    valid = blockchain.verify_wallet_amount(wallet_id, amount)
    if not valid:
        raise WalletException("Not Enough Coins to create the transaction")

    blockchain.subtract_from_wallet(wallet_id, amount)
    blockchain.add_to_wallet(receiver, amount)

    return jsonify(valid=valid), HttpCode.OK.value


@app.route('/wallet/balance', methods=['GET'])
def get_wallet_amount():
    """
    endpoint to fetch the ballence of a walllet

            Parameters: from request:

                    umnetId (string): the umnetId (wallet id) to get the balance for

            Returns:
                    status code and json data containing:
                        amount (float) : The current amount for the wallet

                        -or-

                        error message
    """
    try:
        data = request.get_json(force=True)
        wallet_id = data["umnetId"].upper()
        amount = blockchain.get_wallet_amount(wallet_id)
        return jsonify(amount=amount), HttpCode.OK.value

    except KeyError as error:
        raise IncorrectPayloadException() from error


@app.errorhandler(WalletException)
def handle_wallet_exception(error):
    """
    Method to handle wallet exception

            Parameters:
                    error: The error that occured in the endpoint

            Returns:
                    error message as json and return code
    """
    return jsonify(error=error.message), HttpCode.BAD_REQUEST.value


@app.errorhandler(IncorrectPayloadException)
def handle_incorrect_payload_exception(error):
    """
    Method to handle incorrect payload exception

            Parameters:
                    error: The error that occured in the endpoint

            Returns:
                    error message with faillure return code
    """
    return jsonify(error=error.json_message), error.return_code
