from src import app
from flask import request, jsonify
import requests
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

json_headers = {'Content-Type': 'application/json'}

@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"

@cross_origin()
@app.route("/create", methods=['POST'])
def createWallet():
    data = request.get_json(force=True)
    
    if (data is None) or ("walletId" not in data):
        return jsonify(error=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    response = requests.post(
        "http://blockchain:5000/wallet/addWallet", json=data)

    return jsonify(response.json()), response.status_code

@cross_origin()
@app.route("/amount", methods=['POST'])
def getWalletAmount():

    data = request.get_json(force=True)

    if (data is None) or ("walletId" not in data):
        return jsonify(error=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value


    response = requests.get(
        "http://blockchain:5000/wallet/balance", json=data)

    return jsonify(response.json()), response.status_code
