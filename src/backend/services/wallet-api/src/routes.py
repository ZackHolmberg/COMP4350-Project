from src import app, cross_origin
from flask import request, jsonify
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.utils import BisonCoinUrls
from shared.exceptions import IncorrectPayloadException, UserNotFoundException 
from shared.utils import send_get_request, send_post_request

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
user_api_url = BisonCoinUrls.user_api_url

@cross_origin()
@app.route("/")
def index():
    return "Hello from your wallet"

@cross_origin()
@app.route("/amount", methods=['POST'])
def getWalletAmount():
    data = request.get_json(force=True)

    if (data is None) or ("umnetId" not in data):
        raise IncorrectPayloadException()

    response = send_get_request( blockchain_wallet_url.format("balance"), data)
    return jsonify(response.json()), response.status_code


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(UserNotFoundException)
def handle_wallet_error(e):
    return jsonify(error=e.json_message), e.return_code

