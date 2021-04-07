import json
import os
import sys

import requests
from flask import jsonify, request
from src import app, cross_origin

if os.environ.get("SERVICE_IN_DOCKER", False):
    sys.path.append(os.path.abspath(os.path.join("..", "")))
else:
    sys.path.append(os.path.abspath(os.path.join("../..", "")))

from shared import HttpCode
from shared.exceptions import (
    BisonCoinException,
    IncorrectPayloadException,
    UserNotFoundException,
)
from shared.utils import BisonCoinUrls, send_get_request, send_post_request

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
user_api_url = BisonCoinUrls.user_api_url
blockchain_url = BisonCoinUrls.blockchain_url


def authenticate_user(umnetId, password):
    req_body = {"umnetId": umnetId, "password": password}
    response = send_post_request(user_api_url.format("authUser"), req_body)
    if "success" not in response.json():
        raise BisonCoinException(
            json_message=response.json(), return_code=response.status_code
        )


@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"


@cross_origin()
@app.route("/amount", methods=["POST"])
def getWalletAmount():
    data = request.get_json()
    try:
        umnetId = data["umnetId"]
        password = data["password"]
    except KeyError:
        raise IncorrectPayloadException()

    authenticate_user(umnetId, password)

    response = send_get_request(blockchain_wallet_url.format("balance"), data)
    return jsonify(response.json()), response.status_code


@cross_origin()
@app.route("/history/<umnetId>", methods=["GET"])
def getWalletHistory(umnetId):

    response = requests.get(blockchain_url.format("chain")).json()
    chain = response["chain"]

    result = []

    umnetId = umnetId.upper()

    for block in chain[1:]:
        block = json.loads(block)
        ts = block["transaction"]["timestamp"]

        # if user was the miner
        if umnetId == block["miner_id"].upper():
            result.append(
                {
                    "transaction": {
                        "timestamp": ts,
                        "amount": block["reward_amount"],
                        "from_address": "BLOCKCHAIN",
                        "to_adderss": block["miner_id"],
                        "id": block["transaction"]["id"],
                        "signature": block["transaction"]["signature"],
                    },
                    "type": "reward",
                }
            )

        # if user was the sender
        if umnetId == block["transaction"]["from_address"].upper():
            result.append({"transaction": block["transaction"], "type": "send"})

        # if user was the reciever
        if umnetId == block["transaction"]["to_address"].upper():
            result.append({"transaction": block["transaction"], "type": "receive"})

    result.reverse()
    return jsonify({"history": result}), HttpCode.OK.value


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(UserNotFoundException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code


@app.errorhandler(BisonCoinException)
def handle_error(e):
    return jsonify(e.json_message), e.return_code
