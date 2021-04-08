import time
from hashlib import sha256

import mock
import pytest
from src import routes
from src.miningpool import MiningPool

VALID_NONCE = 734
VALID_AMOUNT = 3
VALID_ID = "ea269ca4907f920c60eb07bc8be34451ff6f63fef69e969be83b4d29921ff70a"
VALID_SIGNATURE = "1ff49f1e529c7a21a63bb176220457ecfc000051a56079bfbdc2b4d0a56d2a1648593c56b18b0b491207e697540fc1ee7d648f37dd3c235a4f3ceabb9ecd103533d60f6c9bc07de6236325ab992b85a25d65bc83be846b8bae2d5123818cb9cc8cd0e822b3d96fe14bfb2f75e5aa5cfa0302d3b420f5affb0c0c186663747ac0"
VALID_TIMESTAMP = 1616381251
VALID_PROOF = "0000733069633f9c7ff25d8ff0e260709f87117245d1eaa959eb193507741a5b"


@pytest.fixture(scope="function")
def test_receiver():
    receiver = mock.MagicMock()
    return receiver


@pytest.fixture(scope="function")
def test_pool(test_receiver):
    test_pool = MiningPool(test_receiver, True)
    return test_pool


@pytest.fixture(scope="function")
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
        "from": "test2",
        "to": "test1",
        "amount": VALID_AMOUNT,
        "timestamp": VALID_TIMESTAMP,
        "id": VALID_ID,
        "signature": VALID_SIGNATURE,
    }


def teardown_test_transaction():
    routes.difficulty = 4
    routes.ongoing_transaction = None


def test_valid_proof():
    setup_test_transaction()
    hash_ = sha256(
        (
            str(VALID_NONCE)
            + str(VALID_AMOUNT)
            + str(VALID_TIMESTAMP)
            + VALID_ID
            + VALID_SIGNATURE
        ).encode("utf-8")
    ).hexdigest()
    assert hash_ == VALID_PROOF
    assert routes.valid_proof(hash_, VALID_NONCE)
    teardown_test_transaction()


def test_invalid_proof():
    setup_test_transaction()
    hash_ = sha256(
        (str(5) + "test2" + "test3" + str(10) + "test3" + "test4").encode("utf-8")
    ).hexdigest()
    assert not routes.valid_proof(hash_, 5)
    teardown_test_transaction()


def test_invalid_difficulty():
    setup_test_transaction()
    hash_ = sha256(
        (str(5) + "test2" + "test3" + str(10) + "test3" + "test4").encode("utf-8")
    ).hexdigest()
    routes.difficulty = 100
    assert not routes.valid_proof(hash_, 5)
    teardown_test_transaction()
