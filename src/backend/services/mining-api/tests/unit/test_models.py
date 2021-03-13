import pytest
from src.miningpool import MiningPool 
import mock
import time
import threading
import queue
from src.routes import difficulty, ongoing_transaction, valid_proof
from hashlib import sha256

@pytest.fixture(scope='function')
def test_receiver():
    receiver = mock.MagicMock()
    return receiver

@pytest.fixture(scope='function')
def test_pool(test_receiver):
    test_pool = MiningPool(test_receiver, True)
    return test_pool

@pytest.fixture(scope='function')
def test_pool_nm(test_receiver):
    test_pool = MiningPool(test_receiver, False)
    return test_pool

def try_call_check (rcv):
    tries = 0
    while not rcv.called and tries < 3:
        time.sleep(0.5)
        tries += 1

def test_pool_init (test_pool, test_receiver):
    assert test_pool._pool.empty()
    assert not test_pool._mining_thread.is_alive()
    assert test_pool._ready_to_mine
    test_receiver.assert_not_called()

def test_pool_start_mining (test_pool, test_receiver):
    test_pool.start_thread()
    assert test_pool._pool.empty()
    assert test_pool._mining_thread.is_alive()
    assert test_pool._ready_to_mine
    test_receiver.assert_not_called()


def test_enter_new_data(test_pool, test_receiver):
    data = "Test"
    test_pool.add_to_pool(data)
    test_pool.start_thread()
    assert test_pool._mining_thread.is_alive()
    try_call_check(test_receiver)
    test_receiver.assert_called_once_with(data)

def test_enter_new_data_not_ready(test_pool, test_receiver):
    data = "Test"
    test_pool.add_to_pool(data)
    test_pool.start_thread()
    assert test_pool._mining_thread.is_alive()
    try_call_check(test_receiver)
    assert not test_pool._ready_to_mine

def test_ready_to_mine(test_pool_nm):
    assert not test_pool_nm._ready_to_mine
    test_pool_nm.ready_to_mine()
    assert test_pool_nm._ready_to_mine

def setup_test_transaction():
    difficulty = 0
    ongoing_transaction = {"from" : "test1", "to": "test2", "amount": 10, "id":"test3", "signature": "test4"}


def teardown_test_transaction():
    difficulty = 4
    ongoing_transaction = None

def test_valid_proof():
    setup_test_transaction()
    hash_ = sha256((str(5) + "test1" + "test2" + str(10) + "test3" + "test4").encode('utf-8')).hexdigest()
    valid_proof(hash_, 5)
    teardown_test_transaction()

def test_invalid_proof():    
    setup_test_transaction()
    hash_ = sha256((str(5) + "test2" + "test3" + str(10) + "test3" + "test4").encode('utf-8')).hexdigest()
    valid_proof(hash_, 5)
    teardown_test_transaction()


def test_invalid_difficulty():    
    setup_test_transaction()
    hash_ = sha256((str(5) + "test2" + "test3" + str(10) + "test3" + "test4").encode('utf-8')).hexdigest()
    difficulty = 100 
    valid_proof(hash_, 5)
    teardown_test_transaction()
