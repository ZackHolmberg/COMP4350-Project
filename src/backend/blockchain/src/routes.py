from src import app
from .transaction import Transaction
from .block import Block
from .blockchain import blockchain, Blockchain
from .exceptions import WalletException
from flask import request, jsonify
import sys
import os
import json
from src import peers

sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared.exceptions import IncorrectPayloadException
from shared import HttpCode
from shared.utils import send_post_request, send_get_request

request_handlers = {
    "GET": send_get_request,
    "POST": send_post_request
}

def query_peer(peer):
    try:
        # Implement the logic to take the responses and add that to the chain
        response = send_get_request(peer+"/chain", None)
        response = send_get_request(peer+"/wallet/all", None)

    except Exception as e:
        print("LOG: Peer Replication Failed on startup", str(e))

def replicate(route, request_type, request):
    for peer in peers:
        full_route = peer+route
        try:
            response = request_handlers[request_type](full_route,request)
        except Exception as e:
            print("LOG: Replication Failed", route, request_type, request, str(e))

@app.route("/")
def index():
    return "Hello Blockchain"


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.toJSON())
    return jsonify(length=len(chain), chain=chain), HttpCode.OK.value

@app.route('/addPeer', methods=['POST'])
def get_chain():
    data = request.get_json()
    try:
        peer = data["peer"]
        peers.append(peer)
    except KeyError:
        IncorrectPayloadException()

    return jsonify(length=len(chain), chain=chain), HttpCode.OK.value


@app.route('/wallet/all', methods=['GET'])
def get_wallets():
    wallets = []
    for wallet, amount in blockchain.wallets.items():
        wallets.append(json.dumps( {"wallet": wallet, "amount": amount} ))
    
    return jsonify(length=len(wallets), wallets=wallets), HttpCode.OK.value


@app.route('/addBlock', methods=['POST'])
def proof():
    data = request.get_json()
    try:
        new_transaction = Transaction(
            data["from"],
            data["to"],
            data["amount"],
            data["timestamp"],
            data["id"],
            data["signature"]
        )
        miner_id = data["minerId"].upper()
        proof = data["proof"]
        nonce = data["nonce"]

    except KeyError as e:
        raise IncorrectPayloadException()

    new_block = Block(
        len(blockchain.chain),
        new_transaction,
        nonce,
        proof,
        blockchain.get_last_block().hash,
        miner_id,
        Blockchain.COINBASE_AMOUNT
    )

    # We guarantee that all the necessary validation has been done by this point, so simply add the
    # new block to the chain
    blockchain.chain.append(new_block)

    blockchain.add_to_wallet(miner_id, Blockchain.COINBASE_AMOUNT)

    replicate('/addBlock', 'POST', data)
    return jsonify(success=True), HttpCode.CREATED.value


@app.route('/wallet/checkWallet', methods=['POST'])
def check_wallet_exists():
    try:
        data = request.get_json()
        wallet_id = data["umnetId"].upper()
        exists = wallet_id in blockchain.wallets
        return jsonify(valid=exists), HttpCode.OK.value

    except KeyError as e:
        raise IncorrectPayloadException()


@app.route('/wallet/addWallet', methods=['POST'])
def add_wallet():
    try:
        data = request.get_json()
        wallet_id = data["umnetId"].upper()
        success = blockchain.add_wallet(wallet_id)
        
        replicate('/wallet/addWallet', 'POST', data)
        return jsonify(success=success), HttpCode.CREATED.value

    except KeyError as e:
        raise IncorrectPayloadException()


@app.route('/wallet/createTransaction', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        wallet_id = data["from"].upper()
        amount = data["amount"]
        receiver = data["to"].upper()

    except KeyError as e:
        raise IncorrectPayloadException()

    valid = blockchain.verify_wallet_amount(wallet_id, amount)
    if not valid:
        raise WalletException("Not Enough Coins to create the transaction")

    blockchain.subtract_from_wallet(wallet_id, amount)
    blockchain.add_to_wallet(receiver, amount)

    replicate('/wallet/createTransaction', 'POST', data)
    return jsonify(valid=valid), HttpCode.OK.value


@app.route('/wallet/balance', methods=['GET'])
def get_wallet_amount():
    try:
        data = request.get_json(force=True)
        wallet_id = data["umnetId"].upper()
        amount = blockchain.get_wallet_amount(wallet_id)
        return jsonify(amount=amount), HttpCode.OK.value

    except KeyError as e:
        raise IncorrectPayloadException()

@app.errorhandler(WalletException)
def handle_wallet_exception(e):
    return jsonify(error=e.message), HttpCode.BAD_REQUEST.value

@app.errorhandler(IncorrectPayloadException)
def handle_wallet_exception(e):
    return jsonify(error=e.json_message), e.return_code
