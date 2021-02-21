from src.transaction import Transaction
from src.block import Block
from src.blockchain import Blockchain
from hashlib import sha256
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


"""
Transaction Tests
"""


def test_transaction_constructor():
    testTransaction = Transaction("toAddress", "fromAddress", 5)
    assert (
        testTransaction.toAddress == "toAddress" and
        testTransaction.fromAddress == "fromAddress" and
        testTransaction.amount == 5)


"""
Block Tests
"""


def test_block_constructor():
    testIndex = 0
    testTransaction = Transaction(
        "toAddress", "fromAddress", 5)
    print("In test_block_constructor", type(testTransaction))
    testTimestamp = datetime.now().time().strftime("%m/%d/%Y, %H:%M:%S")
    testPrevHash = "prevHash"

    testBlock = Block(testIndex, testTransaction,
                      testTimestamp, testPrevHash)
    assert (
        testBlock.index == testIndex and
        testBlock.transaction != None and
        testBlock.timestamp == testTimestamp and
        testBlock.prevHash == testPrevHash and
        testBlock.nonce == 0 and
        len(testBlock.hash) != 0)


def test_calculate_hash():
    testIndex = 0
    testTransaction = Transaction(
        "toAddress", "fromAddress", 5)
    testTimestamp = datetime.now().time().strftime("%m/%d/%Y, %H:%M:%S")
    testPrevHash = "prevHash"

    testBlock = Block(testIndex, testTransaction,
                      testTimestamp, testPrevHash)

    assert testBlock.hash == testBlock.calculateHash()


"""
Blockchain Tests
"""


def test_blockchain_constructor():
    testBlockchain = Blockchain()
    assert len(testBlockchain.chain) == 1


def test_get_last_block():
    print()


def test_append_block_to_chain():
    print()


def test_valid_proof():
    print()


testBlockchain = Blockchain()
testWalletId = "walletId"


def test_add_wallet():
    testBlockchain.addWallet(testWalletId)
    assert testBlockchain.wallets[testWalletId] == 0


def test_add_to_wallet():
    testBlockchain.addToWallet(testWalletId, 5)
    assert testBlockchain.wallets[testWalletId] == 5


def test_subtract_from_wallet():
    testBlockchain.subtractFromWallet(testWalletId, 4)
    assert testBlockchain.wallets[testWalletId] == 1


def test_get_wallet_amount():
    assert testBlockchain.getWalletAmount(testWalletId) == 1
