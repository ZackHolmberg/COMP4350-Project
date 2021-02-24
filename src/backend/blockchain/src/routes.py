from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import blockchain
from flask import request, jsonify
import sys
import os

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
    return jsonify(length=len(chain), chain=chain), HttpCode.OK


@app.route('/proof', methods=['POST'])
def proof():
    data = request.get_json()
    # proof = data["proof"]
    # newBlock = Block()
    # TODO: Get other block data from the request data, including the
    # transaction amount and to/from wallet IDs
    # Then, add/subtract the transaction amount from the respective walletIds
    # Using blockchain.addToWallet and blockchain.subtractFromWallet
    return "proof was hit. You sent:"+request.get_json()


@app.route('/wallet/addWallet', methods=['POST'])
def addWallet():
    try:
        data = request.get_json()
        print(data)
        walletId = data["walletId"]
        success = blockchain.add_wallet(walletId)
        return jsonify(success=success), HttpCode.CREATED
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST


@app.route('/wallet/verifyAmount', methods=['POST'])
def verifyAmount():
    try:
        data = request.get_json()
        walletId = data["walletId"]
        amount = data["amount"]
        valid = blockchain.verify_wallet_amount(walletId, amount)
        return jsonify(valid=valid), HttpCode.OK
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST


@app.route('/wallet/balance', methods=['POST'])
def getWalletAmount():
    try:
        data = request.get_json()
        walletId = data["walletId"]
        amount = blockchain.get_wallet_amount(walletId)
        return jsonify(amount=amount), HttpCode.OK
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST
