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
from shared import HttpCode

from shared.exceptions import IncorrectPayloadException, UserNotFoundException 
from shared.utils import send_get_request, send_post_request

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
user_api_url = BisonCoinUrls.user_api_url
blockchain_url = BisonCoinUrls.blockchain_url

@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"

@cross_origin()
@app.route("/amount", methods=['POST'])
def getWalletAmount():
    data = request.get_json(force=True)

    if (data is None) or ("umnetId" not in data):
        raise IncorrectPayloadException()

    response = send_get_request( blockchain_wallet_url.format("balance"), data)
    return jsonify(response.json()), response.status_code

@cross_origin()
@app.route("/history", methods=['GET'])
def getWalletHistory():

    umnetId = request.args.get('umnetId')

    if umnetId is None:
        raise IncorrectPayloadException()

    response = requests.get( blockchain_url.format("chain")).json()
    chain = response['chain']

    result = []

    for block in chain[1:]:
        block = json.loads(block)
        ts = float(block["timestamp"])
        
        # if user was the miner 
        if umnetId.upper() == block["miner_id"].upper() :
            result.append({"Timestamp": ts, "from" : "Mining", "amount": block["reward_amount"]})

        # if user was the sender
        if umnetId.upper() == block["transaction"]['from_address'].upper():
            result.append({"Timestamp": ts, "to" : block["transaction"]['to_address'], "amount": block["transaction"]["amount"]})
        
        # if user was the reciever
        if umnetId.upper() == block["transaction"]['to_address'].upper():
            result.append({"Timestamp": ts, "from" : block["transaction"]['from_address'], "amount": block["transaction"]["amount"]})

    result.reverse()
    return jsonify({"history" : result}), HttpCode.OK.value 


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(UserNotFoundException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code

