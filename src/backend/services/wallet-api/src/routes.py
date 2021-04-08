"""Module containing routes for the wallet api service"""

import sys
import os
import json
import requests
from flask import request, jsonify
from flask_cors import cross_origin
from src import app

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.utils import BisonCoinUrls
from shared import HttpCode
from shared.exceptions import IncorrectPayloadException, UserNotFoundException, BisonCoinException
from shared.utils import send_get_request, send_post_request

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
user_api_url = BisonCoinUrls.user_api_url
blockchain_url = BisonCoinUrls.blockchain_url


def authenticate_user(umnetId, password):
    """
    Authentication endpoint for services

            Parameters: through request:
                    umnetId (string): A string umnetId that is to be retrieved
                    password (string): The password associated to the supplied umnetId

            Returns:
                    success (boolean): True if user is authenticated, else false
                    error (string): error with the approptiate message
    """
    req_body = {"umnetId": umnetId, "password": password}
    response = send_post_request(user_api_url.format("authUser"), req_body)
    if "success" not in response.json():
        raise BisonCoinException(
            json_message=response.json(), return_code=response.status_code)


@cross_origin()
@app.route("/")
def index():
    """
    Endpoint to check if the service is up

            Parameters: through request:
                    None

            Returns:
                    Greeting string for user
    """
    return "Hello from your wallet"


@cross_origin()
@app.route("/amount", methods=['POST'])
def get_wallet_amount():
    """
    fetches the current amount of the wallet associated with the supplied umnetid and password

            Parameters: through request:
                    umnetId (string): A string umnetId that is to be retrieved
                    password (string): The password associated to the supplied umnetId

            Returns:
                    success (string): json string containing the wallet balance
                    error (string): error with the approptiate message
    """
    data = request.get_json()
    try:
        umnetId = data["umnetId"]
        password = data["password"]
    except KeyError as error:
        raise IncorrectPayloadException() from error

    authenticate_user(umnetId, password)

    response = send_get_request(blockchain_wallet_url.format("balance"), data)
    return jsonify(response.json()), response.status_code


@cross_origin()
@app.route("/history/<umnetId>", methods=['GET'])
def get_wallet_history(umnetId):
    """
    transaction history endpoint for the wallet associated to the supplied umnetId

            Parameters: through request:
                    umnetId (string): A string umnetId that is to be retrieved

            Returns:
                    history (list): a list containing the transaction history of the wallet
                    error (string): error with the approptiate message
    """
    response = requests.get(blockchain_url.format("chain")).json()
    chain = response['chain']

    result = []

    umnetId = umnetId.upper()

    for block in chain[1:]:
        block = json.loads(block)
        time_stamp = block["transaction"]["timestamp"]

        # if user was the miner
        if umnetId == block["miner_id"].upper():
            result.append({"transaction": {"timestamp": time_stamp,
                                           "amount": block["reward_amount"],
                                           "from_address": "BLOCKCHAIN",
                                           "to_adderss": block["miner_id"],
                                           "id": block["transaction"]["id"],
                                           "signature": block["transaction"]["signature"]},
                           "type": "reward"})

        # if user was the sender
        if umnetId == block["transaction"]['from_address'].upper():
            result.append(
                {"transaction": block["transaction"], "type": "send"})

        # if user was the reciever
        if umnetId == block["transaction"]['to_address'].upper():
            result.append(
                {"transaction": block["transaction"], "type": "receive"})

    result.reverse()
    return jsonify({"history": result}), HttpCode.OK.value


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(UserNotFoundException)
def handle_wallet_error(error):
    """
    method to handle incorrect payload and user not found exception

            Parameters:
                    error: The error that occured in the endpoint

            Returns:
                    error message with faillure return code
    """
    return jsonify(error=error.json_message), error.return_code


@app.errorhandler(BisonCoinException)
def handle_error(error):
    """
    method to handle bison coin execptions

            Parameters: through request:
                    error: The error that occured in the endpoint

            Returns:
                    error message with faillure return code
    """
    return jsonify(error.json_message), error.return_code
