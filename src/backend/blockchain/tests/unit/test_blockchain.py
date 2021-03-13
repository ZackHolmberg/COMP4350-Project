from src.transaction import Transaction
from src.block import Block
from src.blockchain import Blockchain
from hashlib import sha256
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


"""
Transaction Tests
"""


def test_transaction_constructor():
    test_transaction = Transaction("fromAddress", "toAddress", 5)
    assert (
        test_transaction.to_address == "toAddress" and
        test_transaction.from_address == "fromAddress" and
        test_transaction.amount == 5)


"""
Block Tests
"""


def test_block_constructor():
    test_index = 0
    test_transaction = Transaction(
        "toAddress", "fromAddress", 5)
    test_timestamp = time.time()
    test_nonce = 0
    test_hash = "0000abc"
    test_prev_hash = "prevHash"
    test_miner_id = "miner_id"
    test_reward = 5

    test_block = Block(test_index, test_transaction,
                       test_timestamp, test_nonce, test_hash, test_prev_hash, test_miner_id, test_reward)
    assert (
        test_block.index == test_index and
        test_block.transaction != None and
        test_block.timestamp == test_timestamp and
        test_block.nonce == 0 and
        len(test_block.hash) != 0 and
        test_block.prev_hash == test_prev_hash and
        test.miner_id == "miner_id" and
        test_reward == 5
    )


"""
Blockchain Tests
"""


def test_blockchain_constructor():
    test_temp_blockchain = Blockchain()
    assert len(test_temp_blockchain.chain) == 1


test_blockchain = Blockchain()


def test_get_last_block():
    assert test_blockchain.get_last_block().index == 0


def test_append_block_to_chain():
    test_index = 0
    test_transaction = Transaction(
        "toAddress", "fromAddress", 5)
    test_timestamp = time.time()
    test_nonce = 0
    test_hash = "0000abc"
    test_prev_hash = "prevHash"
    test_miner_id = "miner_id"
    test_reward = 5

    test_block = Block(test_index, test_transaction,
                       test_timestamp, test_nonce, test_hash, test_prev_hash, test_miner_id, test_reward)
    test_blockchain.append_block_to_chain(test_block, "0000abcdefg")
    assert len(test_blockchain.chain) == 2


test_wallet_id = "walletId"


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
