from src import app
from flask import request, jsonify
import requests
import base64
import sys
import os
from flask_cors import CORS, cross_origin

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString


@cross_origin()
@app.route("/")
def index():
    return "Hello Transactions"


@cross_origin()
@app.route("/create", methods=['POST'])
def createTransaction():
    data = request.get_json()

    try:
        from_address = data["from"]
        to_address = data["to"]
        amount = data["amount"]

    except Exception as e:
        return jsonify(err=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    try:
        isVerified = True
        # TODO do verification if the user is logged in/ the other user exists etc

    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value

    if not isVerified:
        return jsonify(err=FailureReturnString.TRANSACTION_VERFICATION_FAILURE.value), HttpCode.UNAUTHORIZED.value

    req_body = {"walletId": from_address, "amount": amount}

    response = requests.post( "http://blockchain:5000/wallet/verifyAmount", json=req_body)

    if response.status_code is not HttpCode.OK.value:
        return jsonify(response.json()), response.status_code

    response = requests.post( "http://mining:5000/queue", json=data)
    
    if response.status_code is not HttpCode.OK.value:
        return jsonify(response.json()), response.status_code

    req_body = {"walletId": from_address}    
    response = requests.post( "http://blockchain:5000/wallet/verifyAmount", json=req_body)

    try:
        remaining_balance = float(response.json()["amount"]) - float(amount)
        return jsonify(success=True, remaining_balance=remaining_balance), HttpCode.CREATED.value
    
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value
