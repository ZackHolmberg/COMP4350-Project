from src import app
from flask import request, jsonify
from ecdsa import SigningKey, VerifyingKey
import requests
import base64
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString


def validateSignature(id, signature, address):
    public_key = base64.b64decode(address)
    signature = base64.b64decode(signature)

    vk = VerifyingKey.from_string(public_key)

    return vk.verify(signature, id.encode())


@app.route("/")
def index():
    return "Hello Transactions"


@app.route("/create", methods=['POST'])
def createTransaction():
    data = request.get_json()

    try:
        transaction_id = data["id"]
        from_address = data["from"]
        to_address = data["to"]
        amount = data["amount"]
        signature = data["signature"]

    except Exception as e:
        return jsonify(err=FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    try:
        isVerified = validateSignature(transaction_id, signature, from_address)

    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST

    if not isVerified:
        return jsonify(err=FailureReturnString.TRANSACTION_VERFICATION_FAILURE), HttpCode.UNAUTHORIZED

    
    req_body = {"walletId": from_address, "amount": amount}

    response = requests.post("http://blockchain:5000/wallet/verifyAmount", json=req_body)

    if response.status_code is not HttpCode.OK:   
        return jsonify( response.json() ), response.status_code
    

    # TODO call the mining service to initiate a mining

    return jsonify(success=True), HttpCode.CREATED
