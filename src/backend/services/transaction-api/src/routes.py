from src import app, cross_origin
from flask import request, jsonify
import sys
import os
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import codecs

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.exceptions import IncorrectPayloadException, TransactionVerificationException, BisonCoinException, ReceiverException
from shared.utils import send_get_request, send_post_request, BisonCoinUrls
from shared import HttpCode, FailureReturnString

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
mining_url = BisonCoinUrls.mining_url
user_api_url = BisonCoinUrls.user_api_url

###########################################
# TRANSACTION SIGN VERIFICATION
###########################################

def validate_signature(id, signature, address):

    try:
        public_key = RSA.import_key(address)
        unhexify = codecs.getdecoder('hex')
        signature = unhexify(signature.encode("utf-8"))[0]

        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(SHA256.new(str.encode(id)), signature)

        return verified

    except Exception as e:
        raise TransactionVerificationException(json_message=str(e))

##########################################
# SERVICE REQUESTS
#########################################

def create_wallet_transaction(address, amount, receiver, timestamp):
    req_body = {"from": address, "amount": amount,
                "to": receiver, "timestamp": timestamp, }

    response = send_post_request(
        blockchain_wallet_url.format("createTransaction"), req_body)

    if response.status_code is not HttpCode.CREATED.value:        
        raise BisonCoinException(response.json(), response.status_code)


def send_to_mine(body):
    response = send_post_request(mining_url.format("queue"), body)

    if response.status_code is not HttpCode.OK.value:
        raise BisonCoinException(response.json(), response.status_code)


def get_remaining_wallet_amount(address, amount):
    req_body = {"umnetId": address}
    response = send_get_request(
        blockchain_wallet_url.format("balance"), req_body)

    return float(response.json()["amount"])


def verify_receiver(address):
    req_body = {"umnetId": address}
    response = send_post_request(
        blockchain_wallet_url.format("checkWallet"), req_body)

    try:
        valid = response.json()["valid"]
        if not valid:
            raise ReceiverException()
    except KeyError:
        raise BisonCoinException(response.json(), response.status_code)

def retrieve_public_key (umnetId):
    response = send_get_request( user_api_url.format("umnetId/"+ umnetId.upper()), None)
    try:
        data = response.json()
        public_key = data["data"]["public_key"]
        return public_key
    except KeyError:
        raise TransactionVerificationException(json_message=FailureReturnString.PUBLIC_KEY_NF.value)

########################################
# ROUTES
########################################

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
        timestamp = data["timestamp"]
        transaction_id = data["id"]
        signature = data["signature"]

    except KeyError:
        raise IncorrectPayloadException()

    from_address_pk = retrieve_public_key (from_address) 

    isVerified = validate_signature(transaction_id, signature, from_address_pk)
    if not isVerified:
        raise TransactionVerificationException()

    verify_receiver(to_address)
    create_wallet_transaction(from_address, amount, to_address, timestamp)

    send_to_mine(data)
    remaining_amount = get_remaining_wallet_amount(from_address, amount)

    return jsonify(success=True, remaining_amount=remaining_amount), HttpCode.CREATED.value


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(TransactionVerificationException)
@app.errorhandler(ReceiverException)
def handle_transactions_error(e):
    return jsonify(error=e.json_message), e.return_code

@app.errorhandler(Exception)
def handle_request_error(e):
    return jsonify(error=str(e)), BisonCoinException.client_error

@app.errorhandler(BisonCoinException)
def handle_bisoncoin_error(e):
    return jsonify(e.json_message), e.return_code
