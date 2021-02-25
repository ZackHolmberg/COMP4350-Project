from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import blockchain
from flask import request, jsonify
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode

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
    proof = data["proof"]
    try :
        new_transaction = Transaction(
            data["from_address"], 
            data["to_address"], 
            data["amount"]
        )
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.INCORRECT_PAYLOAD.value

    new_block = Block(
                len(blockchain.chain), 
                new_transaction, 
                time.time(), 
                blockchain.get_last_block().hash, 
                "somehash" )
    
    
    blockchain.subtract_from_wallet(new_transaction.from_address, new_transaction.amount)
    blockchain.add_to_wallet(new_transaction.to_address, new_transaction.amount)

    blockchain.append_block_to_chain(new_block, proof)
    return jsonify(success=True), HttpCode.CREATED.value


@app.route('/wallet/addWallet', methods=['POST'])
def addWallet():
    try:
        data = request.get_json()
        walletId = data["walletId"]
        success = blockchain.add_wallet(walletId)
        return jsonify(success=success), HttpCode.CREATED.value
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value


@app.route('/wallet/verifyAmount', methods=['POST'])
def verifyAmount():
    try:
        data = request.get_json()
        walletId = data["walletId"]
        amount = data["amount"]
        valid = blockchain.verify_wallet_amount(walletId, amount)
        return jsonify(valid=valid), HttpCode.OK.value
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value


@app.route('/wallet/balance', methods=['GET'])
def getWalletAmount():
    try:
        data = request.get_json()
        walletId = data["walletId"]
        amount = blockchain.get_wallet_amount(walletId)
        return jsonify(amount=amount), HttpCode.OK.value
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value
