from src import app
from flask import request, jsonify
import requests
import sys, os
import json

if os.environ.get('SERVICE_IN_DOCKER',False):             
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString

json_headers = {'Content-Type': 'application/json'}

@app.route("/")
def index():
    return "Hello from your wallet"


@app.route("/create", methods = ['POST'])
def createWallet():
    data = request.get_json(force=True)

    if (data is None) or ("public_key" not in data):
        return jsonify(error = FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    req_body = {"walletId": data["public_key"]}

    response = requests.post("http://blockchain:5000/wallet/addWallet", json=req_body)

    return jsonify( response.json() ), HttpCode.CREATED
    


@app.route("/amount", methods = ['POST'])
def getWalletAmount():
    
    data = request.get_json(force=True)

    
    if (data is None) or ("public_key" not in data):
        return jsonify(error = FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    req_body = {"walletId": data["public_key"]}

    response = requests.post("http://blockchain:5000/wallet/balance", json=req_body)

    return jsonify( response.json() ), HttpCode.OK
    