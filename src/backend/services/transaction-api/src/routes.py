from src import app
from flask import request, jsonify
import requests
import sys
import os
from flask_cors import CORS, cross_origin
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import codecs

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString

def validateSignature(id, signature, address):
    public_key = RSA.import_key(address)
    unhexify = codecs.getdecoder('hex')
    signature = unhexify(signature.encode("utf-8"))[0]

    verifier = PKCS1_v1_5.new(public_key)
    verified = verifier.verify(SHA256.new(str.encode(id)), signature)
    
    return verified


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
        transaction_id = data["id"]
        signature = data["signature"]

    except Exception as e:
        return jsonify(err=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    try:
        isVerified = validateSignature(transaction_id, signature, from_address)
        # TODO do verification if the user is logged in/ the other user exists etc
        
        if not isVerified:
            return jsonify(err=FailureReturnString.SIGNATURE_VERFICATION_FAILURE.value), HttpCode.BAD_REQUEST.value

    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value

    if not isVerified:
        return jsonify(err=FailureReturnString.TRANSACTION_VERFICATION_FAILURE.value), HttpCode.UNAUTHORIZED.value

    req_body = {"walletId": from_address, "amount": amount}

    response = requests.post( "http://blockchain:5000/wallet/verifyAmount", json=req_body)

    if response.status_code is not HttpCode.OK.value or not response.json()["valid"]:
        return jsonify(err=FailureReturnString.WALLET_VERFICATION_FAILURE.value), HttpCode.BAD_REQUEST.value

    response = requests.post( "http://mining:5000/queue", json=data)
    
    if response.status_code is not HttpCode.OK.value:
        return jsonify(response.json()), response.status_code

    req_body = {"walletId": from_address}    
    response = requests.get( "http://blockchain:5000/wallet/balance", json=req_body)

    try:
        remaining_balance = float(response.json()["amount"]) - float(amount)
        return jsonify(success=True, remaining_balance=remaining_balance), HttpCode.CREATED.value
    
    except Exception as e:
        return jsonify(err=str(e)), HttpCode.BAD_REQUEST.value
