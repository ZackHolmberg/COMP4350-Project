"routes for the transaction service api"
import sys
import os
import codecs
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from flask import request, jsonify
from flask_cors import cross_origin
from src import app

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.exceptions import IncorrectPayloadException,\
    TransactionVerificationException, BisonCoinException, ReceiverException
from shared.utils import send_get_request, send_post_request, BisonCoinUrls
from shared import HttpCode, FailureReturnString

blockchain_wallet_url = BisonCoinUrls.blockchain_wallet_url
mining_url = BisonCoinUrls.mining_url
user_api_url = BisonCoinUrls.user_api_url

###########################################
# TRANSACTION SIGN VERIFICATION
###########################################


def validate_signature(id, signature, address):
    """
    Method to validate a transaction's signature

            Parameters:
                    id (string): The id of the transaction
                    signature (string): The signature of the transaction
                    address (string): the public key

            Returns:
                    Verifies (bool): true if verified else false
    """
    try:
        public_key = RSA.import_key(address)
        unhexify = codecs.getdecoder('hex')
        signature = unhexify(signature.encode("utf-8"))[0]

        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(SHA256.new(str.encode(id)), signature)

        return verified

    except Exception as error:
        raise TransactionVerificationException(json_message=str(error)) from error

##########################################
# SERVICE REQUESTS
#########################################


def create_wallet_transaction(address, amount, receiver, timestamp):
    """
    Method to create a wallet's transaction

            Parameters:
                    address (string): the public key
                    reciever (string): the reciever of the transaction
                    amount (fliat): the amount to be sent
                    timestamp: timestamp of the transaction

            Returns:
                    error message with faillure return code on failure
    """
    req_body = {"from": address, "amount": amount,
                "to": receiver, "timestamp": timestamp, }

    response = send_post_request(
        blockchain_wallet_url.format("createTransaction"), req_body)

    if response.status_code is not HttpCode.OK.value:
        if "error" not in response.json():
            raise BisonCoinException(
                FailureReturnString.TRANSACTION_CREATION_FAILURE.value, response.status_code)
        raise BisonCoinException(
            response.json()["error"], response.status_code)


def send_to_mine(body):
    """
    Method to send a transaction to the mining queue

            Parameters:
                    body (string): the body of the transaction

            Returns:
                    error message with faillure return code on failure
    """
    response = send_post_request(mining_url.format("queue"), body)

    if response.status_code is not HttpCode.OK.value:
        raise BisonCoinException(
            json_message=response.json(), return_code=response.status_code)


def get_remaining_wallet_amount(address):
    """
    Method to get the remaining wallet amount for a user

            Parameters:
                    address (string): address associated to the wallet

            Returns:
                    amount (float): The balance of the wallet
    """
    req_body = {"umnetId": address}
    response = send_get_request(
        blockchain_wallet_url.format("balance"), req_body)

    return float(response.json()["amount"])


def verify_receiver(address):
    """
    Method to verify if the user's wallet exists

            Parameters:
                    address (string): the address of the reciever's wallet

            Returns:
                    exception if validation fails else none
    """
    req_body = {"umnetId": address}
    response = send_post_request(
        blockchain_wallet_url.format("checkWallet"), req_body)

    try:
        valid = response.json()["valid"]
        if not valid:
            raise ReceiverException()
    except KeyError as error:
        raise BisonCoinException(json_message=response.json(), return_code=response.status_code)\
            from error


def retrieve_public_key(umnetId):
    """
    Method to get the public key associated to a particular umnetId

            Parameters: through request:
                    umnetId(string): The id associated to the public key

            Returns:
                    public_key(string): the pblic key for the supplied id
                    raises error on transaction verification failure
    """
    response = send_get_request(user_api_url.format("umnetId/" + umnetId.upper()), None)
    try:
        data = response.json()
        public_key = data["data"]["public_key"]
        return public_key
    except KeyError as error:
        raise TransactionVerificationException(
            json_message=FailureReturnString.PUBLIC_KEY_NF.value) from error

########################################
# ROUTES
########################################


@cross_origin()
@app.route("/")
def index():
    """
    Route that returns a greeting if the service is up
    """
    return "Hello Transactions"


@cross_origin()
@app.route("/create", methods=['POST'])
def create_transaction():
    """
    endpoint to create a new transaction

            Parameters: through request:
                    from_address (string): the sender's address
                    to_address (string): the reciever's address
                    amount (float): the amount for the transaction
                    timestamp (float): the timestamp of the transaction
                    transaction_id (string): the id of the transaction
                    signature (string): The signature of the transaction

            Returns:
                    success (boolean): true on success else false
                    remaining amount (float): the remaining wallet amount
                    raises an error in case of failure
    """
    data = request.get_json()

    try:
        from_address = data["from"]
        to_address = data["to"]
        amount = data["amount"]
        timestamp = data["timestamp"]
        transaction_id = data["id"]
        signature = data["signature"]

    except KeyError as error:
        raise IncorrectPayloadException() from error
    from_address_pk = retrieve_public_key(from_address)

    is_verified = validate_signature(transaction_id, signature, from_address_pk)
    if not is_verified:
        raise TransactionVerificationException()

    verify_receiver(to_address)
    create_wallet_transaction(from_address, amount, to_address, timestamp)

    send_to_mine(data)
    remaining_amount = get_remaining_wallet_amount(from_address)

    return jsonify(success=True, remaining_amount=remaining_amount), HttpCode.CREATED.value


@app.errorhandler(IncorrectPayloadException)
@app.errorhandler(TransactionVerificationException)
@app.errorhandler(BisonCoinException)
@app.errorhandler(ReceiverException)
def handle_transactions_error(error):
    """
    Method to handle user reciever, verification, bisoncoin, and incorrect payload
    exceptions

            Parameters: through request:
                    error: The error that occured in the endpoint

            Returns:
                    error message as json and return code
    """
    return jsonify(error=error.json_message), error.return_code


@app.errorhandler(Exception)
def handle_request_error(error):
    """
    method to handle general errors

            Parameters: through request:
                    error: The error that occured in the endpoint

            Returns:
                    error message as json and return code
    """
    return jsonify(error=str(error)), BisonCoinException.client_error
