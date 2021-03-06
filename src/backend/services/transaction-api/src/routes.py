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

from shared.exceptions import IncorrectPayloadException, TransactionVerificationException, BisonCoinException, WalletVerificationException, ReceiverException
from shared.utils import send_get_request, send_post_request, BisonCoinUrls
from shared import HttpCode

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
mining_url = BisonCoinUrls.mining_url

################################
# Transaction Sign Verification
################################

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

##############################
# Service Requests
##############################

def verify_wallet_amount(address, amount):
    req_body = {"walletId": address, "amount": amount}

    response = send_post_request(blockchain_wallet_url.format("verifyAmount"), req_body)

    if response.status_code is not HttpCode.OK.value or not response.json()["valid"]:
        raise WalletVerificationException()

def send_to_mine(body):
    response = send_post_request(mining_url.format("queue"), body)
    
    if response.status_code is not HttpCode.OK.value:
        raise BisonCoinException(json_message=response.json(), return_code=response.status_code)

def get_remaining_wallet_amount(address, amount):
    req_body = {"walletId": address}    
    response = send_get_request(blockchain_wallet_url.format("balance"), req_body)

    return float(response.json()["amount"]) - float(amount)

def verify_receiver(address):
    req_body = {"walletId": address}    
    response = send_post_request( blockchain_wallet_url.format("checkWallet"), req_body)

    try:
        valid = response.json()["valid"]
        if not valid:
            raise ReceiverException()
    except KeyError as e:
        raise IncorrectPayloadException()


####################
# Routes
###################

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

    except KeyError as e:
        raise IncorrectPayloadException()

    isVerified = validate_signature(transaction_id, signature, from_address)
    if not isVerified:
        raise TransactionVerificationException() 

    # TODO do verification if the user is logged in
    verify_wallet_amount(from_address, amount)
    verify_receiver(to_address)

    send_to_mine(data)

    remaining_amount = get_remaining_wallet_amount(from_address, amount)
    return jsonify(success=True, remaining_amount=remaining_amount), HttpCode.CREATED.value


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(TransactionVerificationException)
@app.errorhandler(WalletVerificationException)
@app.errorhandler(BisonCoinException)
@app.errorhandler(ReceiverException)
def handle_transactions_error(e):
    return jsonify(error=e.json_message) , e.return_code

@app.errorhandler(Exception)
def handle_request_error(e):
    return jsonify(error=str(e)), BisonCoinException.client_error 
