import json
import os
import sys

import pytest
import src
from pytest_mock import mocker
from src import app

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from shared import FailureReturnString

mimetype = "application/json"
headers = {"Content-Type": mimetype, "Accept": mimetype}

NO_WALLET = "no corresponding wallet for id"
NOT_ENOUGH_COINS = "Not Enough Coins to create the transaction"
WALLET_EXISTS = "wallet ID already exists"


@pytest.fixture(scope="module")
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


@pytest.fixture(scope="module")
def initial_chain():
    return [
        src.Block(
            0, src.Transaction("", "", 0, 0, "", ""), 0, "0000", "0", "miner_id", 0
        )
    ]


@pytest.fixture(scope="module")
def test_block_payload():
    payload = {
        "from": "user1",
        "to": "user2",
        "amount": 20,
        "timestamp": 404,
        "id": "this_is_the_id",
        "signature": "fake_signature_lol",
        "minerId": "user3",
        "proof": "already_validated",
        "nonce": 10,
    }
    return payload


@pytest.fixture(scope="module")
def test_transaction_payload():
    return {
        "from": "fake_wallet_id",
        "amount": 0,
        "to": "another",
        "timestamp": 0,
        "id": "abc",
        "signature": "123",
    }


def test_index(test_client):
    url = "/"
    response = test_client.get(url)
    assert b"Hello Blockchain" in response.data


def test_check_wallet_exists_Incorrect_payload(test_client):
    url = "/wallet/checkWallet"
    data = {"invalid": "invalid"}
    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data


def test_check_wallet_exists_doesnt_exist(test_client):
    url = "/wallet/checkWallet"
    data = {"umnetId": "invalid"}
    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    assert not response.json["valid"]


def test_check_wallet_exists_does_exist(test_client, mocker):
    mocker.patch.object(src.routes.blockchain, "wallets", {"TESTID": 99})

    url = "/wallet/checkWallet"
    data = {"umnetId": "testId"}
    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 200
    assert response.json["valid"]


def test_add_block_incorrect_payload(test_client):
    url = "/addBlock"

    payload = {"from": "user1", "to": "user2", "amount": 20}

    response = test_client.post(url, headers=headers, data=json.dumps(payload))

    assert response.status_code == 400
    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data


def test_add_block_success(test_client, mocker, test_block_payload):
    mocker.patch("src.routes.blockchain.add_to_wallet", return_value=True)

    url = "/addBlock"

    response = test_client.post(
        url, headers=headers, data=json.dumps(test_block_payload)
    )

    assert response.status_code == 201
    assert response.json["success"]


def test_get_chain(test_client, initial_chain, mocker):
    mocker.patch.object(src.routes.blockchain, "chain", initial_chain)
    # test GET query on '/chain' route
    url = "/chain"
    response = test_client.get(url)
    data = json.loads(response.json["chain"][0])
    assert response.status_code == 200
    assert response.json["length"] == 1
    assert data["hash"] == "0000"
    assert data["index"] == 0
    assert data["nonce"] == 0
    assert data["prev_hash"] == "0"
    assert data["transaction"] == {
        "amount": 0,
        "from_address": "",
        "to_address": "",
        "timestamp": 0,
        "id": "",
        "signature": "",
    }
    assert data["miner_id"] == "miner_id"
    assert data["reward_amount"] == 0


def test_get_chain_with_add_block(
    test_client, initial_chain, test_block_payload, mocker
):
    # test GET query on '/chain' route
    mocker.patch.object(src.routes.blockchain, "chain", initial_chain)
    test_add_block_success(test_client, mocker, test_block_payload)

    url = "/chain"
    response = test_client.get(url)
    length = response.json["length"]
    data = response.json["chain"]
    assert length == 2
    assert json.loads(data[0])["hash"] == initial_chain[0].hash
    assert json.loads(data[1])["hash"] == test_block_payload["proof"]


def test_add_wallet(test_client):
    url = "/wallet/addWallet"
    data = {"umnetId": "fake_wallet_id"}

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    assert response.json["success"]

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert response.json["error"] == WALLET_EXISTS


def test_add_wallet_incorrect_payload(test_client):
    url = "/wallet/addWallet"
    data = {"notumnetId": "fake_wallet_id"}

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data


def test_sender_notpresent(test_client, test_transaction_payload):
    test_transaction_payload["from"] = "notpresent"
    url = "/wallet/createTransaction"

    response = test_client.post(
        url, data=json.dumps(test_transaction_payload), headers=headers
    )

    assert response.status_code == 400
    assert NO_WALLET.encode() in response.data


def test_receiver_notpresent(test_client, test_transaction_payload, mocker):
    mocker.patch("src.routes.blockchain.subtract_from_wallet", return_value=True)
    url = "/wallet/createTransaction"

    response = test_client.post(
        url, data=json.dumps(test_transaction_payload), headers=headers
    )

    assert response.status_code == 400
    assert NO_WALLET.encode() in response.data


def test_verify_amount(test_client, mocker):
    mocker.patch.object(src.routes.blockchain, "wallets", {"FAKE": 10, "ANOTHER": 10})
    url = "/wallet/createTransaction"
    data1 = {
        "from": "fake",
        "amount": 0,
        "to": "another",
        "timestamp": 0,
        "id": "abc",
        "signature": "123",
    }

    data2 = {
        "from": "fake",
        "amount": 15,
        "to": "another",
        "timestamp": 0,
        "id": "abc",
        "signature": "123",
    }

    response = test_client.post(url, data=json.dumps(data1), headers=headers)

    assert response.status_code == 201
    assert response.json["success"]

    response = test_client.post(url, data=json.dumps(data2), headers=headers)

    assert response.status_code == 400
    assert NOT_ENOUGH_COINS.encode() in response.data


def test_valid_transaction_flow(test_client):
    url = "/wallet/addWallet"
    data = {"umnetId": "user1"}

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    url = "/wallet/addWallet"
    data = {"umnetId": "user2"}

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    url = "/wallet/createTransaction"
    data = {
        "from": "user1",
        "amount": 5,
        "to": "user2",
        "timestamp": 0,
        "id": "abc",
        "signature": "123",
    }

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    assert response.json["success"]

    data1 = {"umnetId": "user1"}
    data2 = {"umnetId": "user2"}
    url = "/wallet/balance"

    response = test_client.get(url, data=json.dumps(data1), headers=headers)

    assert response.status_code == 200
    assert response.json["amount"] == 5

    response = test_client.get(url, data=json.dumps(data2), headers=headers)

    assert response.status_code == 200
    assert response.json["amount"] == 15


def test_get_wallet_amount(test_client):
    url = "/wallet/balance"
    data1 = {"umnetId": "fake_wallet_id"}
    data2 = {"umnetId": "non_existent_wallet_id"}

    response = test_client.get(url, data=json.dumps(data1), headers=headers)

    assert response.status_code == 200
    assert response.json["amount"] == 10

    response = test_client.get(url, data=json.dumps(data2), headers=headers)

    assert response.status_code == 400
    assert response.json["error"] == NO_WALLET


def test_wallet_all(test_client, mocker):
    test_wallets = {"FAKE": 10, "ANOTHER": 20.5}
    mocker.patch.object(src.routes.blockchain, "wallets", test_wallets)

    url = "/wallet/all"
    response = test_client.get(url)

    assert response.json["length"] == 2
    wallet_one = json.loads(response.json["wallets"][0])
    assert wallet_one["umnetId"] == "FAKE"
    assert wallet_one["amount"] == 10
    wallet_two = json.loads(response.json["wallets"][1])
    assert wallet_two["umnetId"] == "ANOTHER"
    assert wallet_two["amount"] == 20.5
