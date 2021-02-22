from src import app
from flask import request, jsonify
from ecdsa import SigningKey, VerifyingKey
import base64

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode, FailureReturnString
## Global
COINBASE_REWARD = 10

## Temporary
TransactionPool = []
private_keys = {}
public_keys = {}


def validateSignature(id, signature, address):
    public_key = base64.b64decode(address)
    signature = base64.b64decode(signature)

    vk = VerifyingKey.from_string(public_key)
    
    return vk.verify(signature, id.encode())


@app.route("/")
def index():
    return "Hello Transactions"

@app.route("/sign", methods=['POST'])
def sign():

    data = request.get_json()
    try: 
        to_sign = data["to_sign"]
    
    # TODO: when the user service and auth service is implemented make the appropriate calls
    # to get the current user instead of client passing it into the json data
        
        user = data["user"]
    
    # Retrieve the private key from the database
        key = private_keys[user]
    
    except Exception as ex:
        return jsonify(Exception=FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST


    signing_key = SigningKey.from_string(bytes.fromhex(key))
    signature = signing_key.sign(to_sign.encode())
    signature = base64.b64encode(signature)

    return jsonify(to_sign=to_sign, signature=signature.decode()), HttpCode.OK



@app.route("/keygen", methods= ['POST'])
def generatePrivateKey():
    data = request.get_json()

    signing_key = SigningKey.generate()
    try:    
        user = data["user"]

        private_keys[user] = signing_key.to_string().hex()

        # encode the public key to make it shorter
        pubk = signing_key.verifying_key.to_string()
        pubk = base64.b64encode(pubk)

        public_keys[user] = pubk

        return jsonify(success=True), HttpCode.CREATED

    except Exception as e:
        return jsonify(success=False), HttpCode.BAD_REQUEST


@app.route("/address/<user>", methods=['GET'])
def getAddress(user):
    try: 
    
    # TODO: when the user service and auth service is implemented make the appropriate calls
    # to get the current user instead of client passing it into the json data
    # Retrieve the private key from the database
        public_key = public_keys[user]
    
    except Exception as ex:
        return jsonify(Exception=FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    return jsonify(address=public_key.decode()), HttpCode.OK

@app.route("/create", methods=['POST'])
def createTransaction():
    data = request.get_json()

    try:
        transaction_id = data["id"]
        from_address = data["from"]
        to_address = data["to"]
        amount = data["amount"]
        signature = data["signature"]

    except Exception as e:
        return jsonify(Exception= FailureReturnString.INCORRECT_PAYLOAD), HttpCode.BAD_REQUEST

    try:
        isVerified = validateSignature(transaction_id, signature, from_address)

    except Exception as e:
        return jsonify(Exception= str(e)), HttpCode.BAD_REQUEST


    if not isVerified:
        return jsonify(Exception= FailureReturnString.TRANSACTION_VERFICATION_FAILURE), HttpCode.UNAUTHORIZED
    
    # call wallet to confirm if the amount event exists

    # call the mining service to initiate a mining
    
    # call the user service to check if the to address is reachable

    return jsonify(success=True), HttpCode.CREATED