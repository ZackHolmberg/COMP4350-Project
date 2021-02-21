from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import Blockchain, blockchain
from flask import request
import json


@app.route("/")
def index():
    return "Hello Blockchain"


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    return json.dumps({"length": len(chain),
                       "chain": chain})


@app.route('/mine', methods=['POST'])
def mine():

    data = request.json
    newTransaction = Transaction(
        data["toAddress"], data["fromAddress"], data["amount"])
    # TODO
    return newTransaction


@app.route('/proof', methods=['POST'])
def proof():
    data = request.json
    proof = data["proof"]
    # TODO
    return "proof was hit. You sent:"+request.json


@app.route('/wallet/addWallet', methods=['POST'])
def addWallet():
    data = request.json
    walletId = data["walletId"]
    if blockchain.addWallet(walletId):
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'error': "wallet ID already exists"}), 400, {'ContentType': 'application/json'}


@app.route('/wallet/addAmount', methods=['POST'])
def addWalletAmount():
    data = request.json
    walletId = data["walletId"]
    amount = data["amount"]
    newAmount = blockchain.addToWallet(walletId, amount)
    if newAmount == -1:
        return json.dumps({'error': "no corresponding wallet for id"}), 400, {'ContentType': 'application/json'}
    else:
        return json.dumps({'newAmount': newAmount}), 200, {'ContentType': 'application/json'}


@app.route('/wallet/subtractAmount', methods=['POST'])
def subtractWalletAmount():
    data = request.json
    walletId = data["walletId"]
    amount = data["amount"]
    newAmount = blockchain.subtractFromWallet(walletId, amount)
    if newAmount == -1:
        return json.dumps({'error': "no corresponding wallet for id"}), 400, {'ContentType': 'application/json'}
    elif newAmount == -2:
        return json.dumps({'error': "insufficient funds"}), 400, {'ContentType': 'application/json'}
    else:
        return json.dumps({'newAmount': newAmount}), 200, {'ContentType': 'application/json'}


@app.route('/wallet/balance', methods=['GET'])
def getWalletAmount():
    data = request.json
    walletId = data["walletId"]
    amount = blockchain.getWalletAmount(walletId)
    if amount == -1:
        return json.dumps({'error': "no corresponding wallet for id"}), 400, {'ContentType': 'application/json'}
    else:
        return json.dumps({'amount': amount}), 200, {'ContentType': 'application/json'}
