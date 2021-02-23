from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import blockchain
from flask import request, jsonify


@app.route("/")
def index():
    return "Hello Blockchain"


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.toJSON())
    return jsonify(length=len(chain), chain=chain), 200


@app.route('/proof', methods=['POST'])
def proof():
    data = request.json
    # proof = data["proof"]
    # newBlock = Block()
    # TODO: Get other block data from the request data, including the
    # transaction amount and to/from wallet IDs
    # Then, add/subtract the transaction amount from the respective walletIds
    # Using blockchain.addToWallet and blockchain.subtractFromWallet
    return "proof was hit. You sent:"+request.json


@app.route('/wallet/addWallet', methods=['POST'])
def addWallet():
    try:
        data = request.json
        walletId = data["walletId"]
        success = blockchain.add_wallet(walletId)
        return jsonify(success=success), 201
    except Exception as e:
        return jsonify(err=str(e)), 400


@app.route('/wallet/verifyAmount', methods=['POST'])
def verifyAmount():
    try:
        data = request.json
        walletId = data["walletId"]
        amount = data["amount"]
        valid = blockchain.verify_wallet_amount(walletId, amount)
        return jsonify(valid=valid), 200
    except Exception as e:
        return jsonify(err=str(e)), 400


@app.route('/wallet/balance', methods=['GET'])
def getWalletAmount():
    try:
        data = request.json
        walletId = data["walletId"]
        amount = blockchain.get_wallet_amount(walletId)
        return jsonify(amount=amount), 200
    except Exception as e:
        return jsonify(err=str(e)), 400