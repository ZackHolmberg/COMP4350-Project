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

def authenticate_user(umnetId, password):
    req_body = {"umnetID": umnetId, "password": password}
    response = send_post_request( user_api_url.format("authUser"), req_body)
    if "success" not in response.json():
        raise BisonCoinException(json_message=response.json(), return_code=response.status_code)

@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"

@cross_origin()
@app.route("/amount", methods=['POST'])
def getWalletAmount():
    data = request.get_json()
    try:
        umnetId = data["umnetId"]
        password = data["password"]
    except KeyError:
        raise IncorrectPayloadException()
    
    authenticate_user(umnetId, password)

    response = send_get_request( blockchain_wallet_url.format("balance"), data)
    return jsonify(response.json()), response.status_code


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(UserNotFoundException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code

@app.errorhandler(BisonCoinException)
def handle_error(e):
    return jsonify(e.json_message), e.return_code
