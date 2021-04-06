from src.transaction import Transaction
from src.block import Block
from src.blockchain import Blockchain
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


"""
Transaction Tests
"""


def test_transaction_constructor():
    test_transaction = Transaction(
        "fromAddress", "toAddress", 5, 123, "id", "signature")
    assert (
        test_transaction.to_address == "toAddress" and
        test_transaction.from_address == "fromAddress" and
        test_transaction.amount == 5 and
        test_transaction.timestamp == 123 and
        test_transaction.id == "id" and
        test_transaction.signature == "signature")

def test_from_json():
    from_address = "from"
    to_address = "to"
    amount = 10.99
    id_ = "randomid"
    signature = "randomsignature"
    timestamp = 00000

    test_json = {"from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "id": id_,
                "signature" : signature,
                "timestamp": timestamp
                }
    transaction = Transaction.from_json(test_json)
    assert transaction.from_address == from_address
    assert transaction.to_address == to_address
    assert transaction.id == id_
    assert transaction.signature == signature
    assert transaction.amount == amount
    assert transaction.timestamp == timestamp

"""
Block Tests
"""

def test_block_constructor():
    test_index = 0
    test_transaction = Transaction(
        "toAddress", "fromAddress", 5, int(time.time()), "id", "signature")
    test_nonce = 0
    test_hash = "0000abc"
    test_prev_hash = "prevHash"
    test_miner_id = "miner_id"
    test_reward = 5

    test_block = Block(test_index, test_transaction,
                       test_nonce, test_hash, test_prev_hash, test_miner_id, test_reward)
    assert (
        test_block.index == test_index and
        test_block.transaction != None and
        test_block.nonce == 0 and
        len(test_block.hash) != 0 and
        test_block.prev_hash == test_prev_hash and
        test_block.miner_id == "miner_id" and
        test_block.reward_amount == test_reward
    )


def test_from_block_json():
    test_index = 0
    test_nonce = 0
    test_hash = "0000abc"
    test_prev_hash = "prevHash"
    test_miner_id = "miner_id"
    test_reward = 5

    from_address = "from"
    to_address = "to"
    amount = 10.99
    id_ = "randomid"
    signature = "randomsignature"
    timestamp = 00000

    test_json = {
        "transaction" : {"from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "id": id_,
                "signature" : signature,
                "timestamp": timestamp
        },
        "index": test_index,
        "nonce": test_nonce,
        "prev_hash" : test_prev_hash,
        "miner_id" : test_miner_id,
        "reward_amount": test_reward,
        "hash": test_hash
    }
    block = Block.from_json(test_json)
    transaction = block.transaction
    assert block.miner_id == test_miner_id
    assert block.reward_amount == test_reward
    assert block.index == test_index
    assert block.nonce == test_nonce
    assert block.prev_hash == test_prev_hash
    
    assert transaction.from_address == from_address
    assert transaction.to_address == to_address
    assert transaction.id == id_
    assert transaction.signature == signature
    assert transaction.amount == amount
    assert transaction.timestamp == timestamp

"""
Blockchain Tests
"""


def test_blockchain_constructor():
    test_temp_blockchain = Blockchain()
    assert len(test_temp_blockchain.chain) == 1


test_blockchain = Blockchain()


def test_get_last_block():
    assert test_blockchain.get_last_block().index == 0


test_wallet_id = "umnetId"


def test_add_wallet():
    test_blockchain.add_wallet(test_wallet_id)
    assert test_blockchain.wallets[test_wallet_id] == 10


def test_add_to_wallet():
    test_blockchain.add_to_wallet(test_wallet_id, 5)
    assert test_blockchain.wallets[test_wallet_id] == 15


def test_subtract_from_wallet():
    test_blockchain.subtract_from_wallet(test_wallet_id, 4)
    assert test_blockchain.wallets[test_wallet_id] == 11


def test_get_wallet_amount():
    assert test_blockchain.get_wallet_amount(test_wallet_id) == 11


def test_verify_wallet_amount_fail():
    assert not test_blockchain.verify_wallet_amount(test_wallet_id, 10000)


def test_verify_wallet_amount_success():
    assert test_blockchain.verify_wallet_amount(test_wallet_id, 1)


def test_build_wallet_from_peer_response():
    peer_response = {
        "length": 2,
        "wallets": [
            "{\"umnetId\": \"KK2\", \"amount\": 10.99}",
            "{\"umnetId\": \"KK1\", \"amount\": 10}"
        ]
    }
    test_blockchain.build_wallets_from_peer_response(peer_response)
    assert len(test_blockchain.wallets) == 2
    assert test_blockchain.verify_wallet_amount("KK1", 10)
    assert test_blockchain.verify_wallet_amount("KK2", 10.99)


def test_build_wallet_from_peer_response_failure():
    peer_response = {
        "length": 2,
        "wallets": [
            "{\"umnetId\": \"Failure3\", \"amount\": 10.99}",
            "{\"umnetId\": \"Failure4\"}"
        ]
    }

    test_blockchain.build_wallets_from_peer_response(peer_response)
    assert len(test_blockchain.wallets) == 2
    assert test_blockchain.verify_wallet_amount("KK1", 10)
    assert test_blockchain.verify_wallet_amount("KK2", 10.99)

def test_build_chain_from_peer_response_failure():
    peer_response = {
    "chain": [
        "{\"hash\": \"1234\", \"miner_id\": \"miner_id_new\", \"nonce\": 123, \"prev_hash\": \"0\", \"reward_amount\": 0, \"transaction\": {\"amount\": 0, \"from_address\": \"from\", \"id\": \"\", \"signature\": \"\", \"timestamp\": 0, \"to_address\": \"to\"}}"
    ],
    "length": 1
    }
    test_blockchain.build_chain_from_peer_response(peer_response)
    assert len(test_blockchain.chain) == 1
    assert test_blockchain.chain[0].hash == "0000"
    assert test_blockchain.chain[0].index == 0
    assert test_blockchain.chain[0].miner_id == "miner_id"
    assert test_blockchain.chain[0].transaction.from_address == ""
    assert test_blockchain.chain[0].transaction.to_address == ""
    

def test_build_chain_from_peer_response():
    peer_response = {
    "chain": [
        "{\"hash\": \"1234\", \"index\": 0, \"miner_id\": \"miner_id_new\", \"nonce\": 123, \"prev_hash\": \"0\", \"reward_amount\": 0, \"transaction\": {\"amount\": 0, \"from_address\": \"from\", \"id\": \"\", \"signature\": \"\", \"timestamp\": 0, \"to_address\": \"to\"}}"
    ],
    "length": 1
    }
    test_blockchain.build_chain_from_peer_response(peer_response)
    assert len(test_blockchain.chain) == 1
    assert test_blockchain.chain[0].hash == "1234"
    assert test_blockchain.chain[0].index == 0
    assert test_blockchain.chain[0].miner_id == "miner_id_new"
    assert test_blockchain.chain[0].transaction.from_address == "from"
    assert test_blockchain.chain[0].transaction.to_address == "to"

def test_build_chain_multiple_chain():
    peer_response = {
    "chain": [
        "{\"hash\": \"1234\", \"index\": 0, \"miner_id\": \"miner_id_new\", \"nonce\": 123, \"prev_hash\": \"0\", \"reward_amount\": 0, \"transaction\": {\"amount\": 0, \"from_address\": \"from\", \"id\": \"\", \"signature\": \"\", \"timestamp\": 0, \"to_address\": \"to\"}}",
        "{\"hash\": \"99\", \"index\": 1, \"miner_id\": \"miner_id_1\", \"nonce\": 123, \"prev_hash\": \"0\", \"reward_amount\": 0, \"transaction\": {\"amount\": 0, \"from_address\": \"from\", \"id\": \"\", \"signature\": \"\", \"timestamp\": 0, \"to_address\": \"to\"}}",
        "{\"hash\": \"4567\", \"index\": 2, \"miner_id\": \"miner_id_2\", \"nonce\": 123, \"prev_hash\": \"0\", \"reward_amount\": 0, \"transaction\": {\"amount\": 0, \"from_address\": \"from\", \"id\": \"\", \"signature\": \"\", \"timestamp\": 0, \"to_address\": \"to\"}}"
    ],
    "length": 1
    }
    test_blockchain.build_chain_from_peer_response(peer_response)
    assert len(test_blockchain.chain) == 3
    assert test_blockchain.chain[0].hash == "1234"
    assert test_blockchain.chain[1].hash == "99"
    assert test_blockchain.chain[2].hash == "4567"
    assert test_blockchain.chain[0].index == 0
    assert test_blockchain.chain[1].index == 1
    assert test_blockchain.chain[2].index == 2
    assert test_blockchain.chain[0].miner_id == "miner_id_new"
    assert test_blockchain.chain[1].miner_id == "miner_id_1"
    assert test_blockchain.chain[2].miner_id == "miner_id_2"
    
