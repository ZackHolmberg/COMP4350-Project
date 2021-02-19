from src import app
from flask import request, jsonify
from ecdsa import SigningKey, VerifyingKey

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import HttpCode
## Global
COINBASE_REWARD = 10
INCORRECT_PAYLOAD_MSG = "Please send correct json payload"
VERFICATION_FAILURE= "Unable to Verify the Transaction"

## Temporary
TransactionPool = []
keys = {}

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
    
        key = keys[user]
    
    except Exception as ex:
        return jsonify(Exception=ex), HttpCode.BAD_REQUEST


    signing_key = SigningKey.from_string(bytes.fromhex(key))
    signature = signing_key.sign(to_sign)

    return jsonify(to_sign=tosign, signature=signature), HttpCode.OK



@app.route("/keygen", methods= ['POST'])
def generatePrivateKey():
    data = request.get_json()

    signing_key = SigningKey.generate()
    try:    
        user = data["user"]

        keys[user] = signing_key.to_string().hex()

        return jsonify(success=True), HttpCode.OK

    except Exception as e:
        return jsonify(success=False), HttpCode.BAD_REQUEST

@app.route("/address", methods=['GET'])
def getAddress():
    data = request.get_json()
    try: 
    
    # TODO: when the user service and auth service is implemented make the appropriate calls
    # to get the current user instead of client passing it into the json data
    
        user = data["user"]
    
    # Retrieve the private key from the database
        key = keys[user]
    
    except Exception as ex:
        return jsonify(Exception=INCORRECT_PAYLOAD_MSG), HttpCode.BAD_REQUEST


    signing_key = SigningKey.from_string(bytes.fromhex(key))
    address = signing_key.verifying_key.to_string().hex()

    return jsonify(address=address), HttpCode.OK

def verifySignature(id, signature, address):
    vk = VerifyingKey.from_string(address.encode())
    return vk.verify(id, signature)

@app.route("/new", methods=['POST'])
def createTransaction():
    data = request.get_json()

    try:
        transaction_id = data["id"]
        from_address = data["from"]
        to_address = data["to"]
        amount = data["amount"]
        signature = data["signature"]

    except Exception as e:
        return jsonify(Exception= INCORRECT_PAYLOAD_MSG), HttpCode.BAD_REQUEST

    isVerified = verifySignature(transaction_id, signature, from_address)

    if not isVerified:
        return jsonify(Exception= VERFICATION_FAILURE), HttpCode.UNAUTHORIZED
    
    # call the mining service to initiate a mining
    

    return jsonify(Success=True), HttpCode.CREATED