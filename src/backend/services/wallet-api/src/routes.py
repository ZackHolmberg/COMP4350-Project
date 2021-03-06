from src import app, cross_origin
from flask import request, jsonify
import requests
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.utils import BisonCoinUrls
from shared.exceptions import IncorrectPayloadException

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url

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


@app.errorhandler(IncorrectPayloadException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code

