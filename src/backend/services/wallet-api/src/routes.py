from src import app, cross_origin
from flask import request, jsonify
import json
import requests
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.utils import BisonCoinUrls
from shared.exceptions import IncorrectPayloadException
from shared import HttpCode

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
blockchain_url = BisonCoinUrls.blockchain_url

@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"

@cross_origin()
@app.route("/create", methods=['POST'])
def createWallet():
    data = request.get_json()    
    
    if (data is None) or ("walletId" not in data):
        raise IncorrectPayloadException()
    
    response = requests.post( blockchain_wallet_url.format("addWallet"), json=data)
    return jsonify(response.json()), response.status_code

@cross_origin()
@app.route("/amount", methods=['POST'])
def getWalletAmount():
    data = request.get_json(force=True)

    if (data is None) or ("walletId" not in data):
        raise IncorrectPayloadException()

    response = requests.get( blockchain_wallet_url.format("balance"), json=data)
    return jsonify(response.json()), response.status_code

@cross_origin()
@app.route("/history", methods=['GET'])
def getWalletHistory():

    walletId = request.args.get('walletId')

    if walletId is None:
        raise IncorrectPayloadException()

    response = requests.get( blockchain_url.format("chain")).json()
    chain = response['chain']

    result = []

    for block in chain[1:]:
        block = json.loads(block)
        ts = float(block["timestamp"])
        
        # if user was the miner 
        if walletId.upper() == block["miner_id"].upper() :
            result.append({"Timestamp": ts, "from" : "Mining", "amount": block["reward_amount"]})

        # if user was the sender
        if walletId.upper() == block["transaction"]['from_address'].upper():
            result.append({"Timestamp": ts, "to" : block["transaction"]['to_address'], "amount": block["transaction"]["amount"]})
        
        # if user was the reciever
        if walletId.upper() == block["transaction"]['to_address'].upper():
            result.append({"Timestamp": ts, "from" : block["transaction"]['from_address'], "amount": block["transaction"]["amount"]})

    result.reverse()
    return jsonify({"history" : result}), HttpCode.OK.value 

@app.errorhandler(IncorrectPayloadException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code

