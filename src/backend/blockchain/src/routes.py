from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import blockchain, Blockchain
from .exceptions import WalletException
from flask import request, jsonify
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join('..', '')))
from shared import HttpCode
from shared.exceptions import IncorrectPayloadException

@app.route("/")
def index():
    return "Hello Blockchain"


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.toJSON())
    return jsonify(length=len(chain), chain=chain), HttpCode.OK.value


@app.route('/proof', methods=['POST'])
def proof():
    data = request.get_json()
    proof = '0' * Blockchain.difficulty
    # proof = data["proof"]
    try :
        new_transaction = Transaction(
            data["from"], 
            data["to"], 
            data["amount"]
        )
    except KeyError as e:
        raise IncorrectPayloadException()

    new_block = Block(
                len(blockchain.chain), 
                new_transaction, 
                time.time(), 
                "somehash",
                blockchain.get_last_block().hash)
    

    blockchain.append_block_to_chain(new_block, proof)

    blockchain.subtract_from_wallet(new_transaction.from_address, new_transaction.amount)
    blockchain.add_to_wallet(new_transaction.to_address, new_transaction.amount)
    
    return jsonify(success=True), HttpCode.CREATED.value

@app.route('/wallet/checkWallet', methods=['POST'])
def check_wallet_exists():
    try:
        data = request.get_json()
        wallet_id = data["walledId"]
        
        exists = False
        if wallet_id in blockchain.wallets:
            exists =True
        return jsonify(valid=exists), HttpCode.Ok.value

    except KeyError as e:
        raise IncorrectPayloadException()
    

@app.route('/wallet/addWallet', methods=['POST'])
def add_wallet():
    try:
        data = request.get_json()
        wallet_id = data["walletId"]
        success = blockchain.add_wallet(wallet_id)
        return jsonify(success=success), HttpCode.CREATED.value

    except KeyError as e:
        raise IncorrectPayloadException()


@app.route('/wallet/verifyAmount', methods=['POST'])
def verify_amount():
    try:
        data = request.get_json()
        wallet_id = data["walletId"]
        amount = data["amount"]
        valid = blockchain.verify_wallet_amount(wallet_id, amount)
        return jsonify(valid=valid), HttpCode.OK.value

    except KeyError as e:
        raise IncorrectPayloadException()


@app.route('/wallet/balance', methods=['GET'])
def get_wallet_amount():
    try:
        data = request.get_json()
        wallet_id = data["walletId"]
        amount = blockchain.get_wallet_amount(wallet_id)
        return jsonify(amount=amount), HttpCode.OK.value

    except KeyError as e:
        raise IncorrectPayloadException()

@app.errorhandler(WalletException)
def handle_wallet_exception(e):
    return jsonify(error=e.message) , HttpCode.BAD_REQUEST.value

@app.errorhandler(IncorrectPayloadException)
def handle_wallet_exception(e):
    return jsonify(error=e.json_message) , e.return_code