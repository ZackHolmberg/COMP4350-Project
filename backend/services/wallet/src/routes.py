from src import app
from flask import request, jsonify
import requests
import sys, os
import json

sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode, FailureReturnString

@app.route("/")
def index():
    return "Hello from your wallet"


@app.route("/create", methods = ['POST'])
def createWallet():
    data = request.get_json(force=True)

    if (data is None) or ("public_key" not in data):
        return jsonify(error = FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    req_body = {"walletId": data["public_key"]}

    response = requests.post("http://localhost/blockchain/wallet/addWallet", req_body)

    if response.status_code == HttpCode.OK:
        return jsonify(
            success = json.loads(response.text)["success"]
            ), HttpCode.CREATED
    else:
        return jsonify(
            error = json.loads(response.text)["error"]
        ), HttpCode.BAD_REQUEST



@app.route("/amount", methods = ['POST'])
def getWalletAmount():
    
    data = request.get_json(force=True)

    
    if (data is None) or ("public_key" not in data):
        return jsonify(error = FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    req_body = {"walletId": data["public_key"]}

    response = requests.post("http://localhost/blockchain/wallet/balance", req_body)

    if response.status_code == HttpCode.OK:   
        return jsonify(
            amount = json.loads(response.text)["amount"] 
        ), HttpCode.OK
    else:
        return jsonify(
            error = json.loads(response.text)["error"]
        ), HttpCode.BAD_REQUEST
