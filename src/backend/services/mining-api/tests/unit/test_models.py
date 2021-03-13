import pytest
from src.miningpool import MiningPool
import mock
import time
import threading
import queue
from src import routes
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


def try_call_check(rcv):
    tries = 0
    while not rcv.called and tries < 3:
        time.sleep(0.5)
        tries += 1


def test_pool_init(test_pool, test_receiver):
    assert test_pool._pool.empty()
    assert not test_pool._mining_thread.is_alive()
    assert test_pool._ready_to_mine
    test_receiver.assert_not_called()


def test_pool_start_mining(test_pool, test_receiver):
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
    routes.difficulty = 0
    routes.ongoing_transaction = {
        "from": "test2", "to": "test1", "amount": 1, "id": "d3a5dab0199356d8260b9f94c1b783601b3d337e692d6abca8ad2e8cc8e7c4a7", "signature": "6104ebba3a1df561d522f5f5c165698ae1f0152a3ca1613d5e2d0e5bd606733cc6e60df4bcf3e3d6c791f2b1e1ce217cb498c69d0dbfe563139a81f063b6fdb24421c63765ce34d193ea0a92e0e98132e4d5e992a30c25b622e1d287e524960f49dea74826227a59c17021ae446d4fe87ce491d34d7d6d014bb4c7f2928b6641"}


def teardown_test_transaction():
    routes.difficulty = 4
    routes.ongoing_transaction = None


def test_valid_proof():
    setup_test_transaction()
    hash_ = sha256((str(21624) + str(1) + "d3a5dab0199356d8260b9f94c1b783601b3d337e692d6abca8ad2e8cc8e7c4a7" +
                    "6104ebba3a1df561d522f5f5c165698ae1f0152a3ca1613d5e2d0e5bd606733cc6e60df4bcf3e3d6c791f2b1e1ce217cb498c69d0dbfe563139a81f063b6fdb24421c63765ce34d193ea0a92e0e98132e4d5e992a30c25b622e1d287e524960f49dea74826227a59c17021ae446d4fe87ce491d34d7d6d014bb4c7f2928b6641").encode('utf-8')).hexdigest()
    assert routes.valid_proof(hash_, 21624)
    teardown_test_transaction()


def test_invalid_proof():
    setup_test_transaction()
    hash_ = sha256((str(5) + "test2" + "test3" + str(10) +
                    "test3" + "test4").encode('utf-8')).hexdigest()
    assert not routes.valid_proof(hash_, 5)
    teardown_test_transaction()


def test_invalid_difficulty():
    setup_test_transaction()
    hash_ = sha256((str(5) + "test2" + "test3" + str(10) +
                    "test3" + "test4").encode('utf-8')).hexdigest()
    routes.difficulty = 100
    assert not routes.valid_proof(hash_, 5)
    teardown_test_transaction()
