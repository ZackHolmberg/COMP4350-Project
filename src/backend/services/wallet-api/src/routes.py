from src import app, cross_origin
from flask import request, jsonify
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.utils import BisonCoinUrls
from shared.exceptions import IncorrectPayloadException, UserNotFoundException, BisonCoinException
from shared.utils import send_get_request, send_post_request

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
user_api_url = BisonCoinUrls.user_api_url

def authenticate_user(auth_token, walletId):
    req_body = {"umnetID": walletId, "auth_token": auth_token}
    response = send_post_request( user_api_url.format("authUser"), req_body)
    try: 
        success = response["success"]
    except KeyError:
        raise BisonCoinException(json_message=response.json(), return_code=response.status_code)

@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"

@cross_origin()
@app.route("/create", methods=['POST'])
def createWallet():
    data = request.get_json()    

    try:
        walletId = data["walletId"]
        auth_token = data["auth_token"]
    except KeyError:
        raise IncorrectPayloadException()
    
    authenticate_user(auth_token, walletId)
    
    response = send_get_request( user_api_url.format("umnetID/"+ walletId), None)
    try:
        user_data = response.json()
        success = user_data["success"]
    except KeyError as e:
        raise UserNotFoundException()
    
    response = send_post_request( blockchain_wallet_url.format("addWallet"), data)
    return jsonify(response.json()), response.status_code

@cross_origin()
@app.route("/amount", methods=['POST'])
def getWalletAmount():
    data = request.get_json(force=True)

    try:
        walletId = data["walletId"]
        auth_token = data["auth_token"]
    except KeyError:
        raise IncorrectPayloadException()
    
    authenticate_user(auth_token, walletId)

    response = send_get_request( blockchain_wallet_url.format("balance"), data)
    return jsonify(response.json()), response.status_code


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(UserNotFoundException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code

