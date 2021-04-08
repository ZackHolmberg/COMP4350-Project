import codecs
import json
import os
import sys

import pytest
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import PKCS1_v1_5
from src import app

sys.path.append(os.path.abspath(os.path.join("../..", "")))

from shared import FailureReturnString, HttpCode
from shared.utils import BisonCoinUrls


@pytest.fixture(scope="module")
def key():
    key = RSA.generate(bits=1024, randfunc=get_random_bytes)
    return key


@pytest.fixture(scope="module")
def signing_key(key):
    private_key = key.exportKey()
    return RSA.import_key(private_key)


@pytest.fixture(scope="module")
def public_key(key):
    public_key = key.public_key().exportKey()
    return public_key.decode()


@pytest.fixture(scope="module")
def transaction_id():
    return SHA256.new(str.encode("Test"))


@pytest.fixture(scope="module")
def signature(transaction_id, signing_key):
    signer = PKCS1_v1_5.new(signing_key)
    signature = signer.sign(transaction_id)
    hexify = codecs.getencoder("hex")
    return hexify(signature)[0].decode()


@pytest.fixture(scope="module")
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


@pytest.fixture(scope="module")
def json_header():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    return headers


@pytest.fixture(scope="function")
def requests_mock_transaction(requests_mock, public_key):

    requests_mock.post(
        BisonCoinUrls.blockchain_wallet_url.format("checkWallet"),
        json={"valid": True},
        status_code=HttpCode.OK.value,
    )

    requests_mock.get(
        BisonCoinUrls.user_api_url.format("umnetId/USER1"),
        json={"success": True, "data": {"public_key": public_key}},
        status_code=HttpCode.OK.value,
    )

    requests_mock.post(
        BisonCoinUrls.blockchain_wallet_url.format("createTransaction"),
        json={"valid": True},
        status_code=HttpCode.CREATED.value,
    )

    requests_mock.post(
        BisonCoinUrls.mining_url.format("queue"),
        json={"success": True},
        status_code=HttpCode.OK.value,
    )

    requests_mock.get(
        BisonCoinUrls.blockchain_wallet_url.format("balance"),
        json={"amount": 0},
        status_code=HttpCode.OK.value,
    )

    return requests_mock


@pytest.fixture(scope="function")
def correct_payload(signature):
    data = {
        "id": "Test",
        "from": "user1",
        "timestamp": 0,
        "to": "user2",
        "amount": 99,
        "signature": signature,
    }

    return data


def test_home_page(test_client):
    # test GET query on '/' route
    url = "/"
    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert b"Hello Transactions" in response.data


def test_create_transaction_incorrect_payload(
    test_client, json_header, requests_mock_transaction
):
    requests_mock_transaction.post(
        BisonCoinUrls.blockchain_wallet_url.format("createTransaction"),
        json={"valid": False},
        status_code=400,
    )

    data = {
        "from": "user1",
        "to": "user2",
    }
    url = "/create"
    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data


def test_create_transaction_wrong_wallet_amount(
    test_client, json_header, requests_mock_transaction, correct_payload
):

    requests_mock_transaction.post(
        BisonCoinUrls.blockchain_wallet_url.format("createTransaction"),
        json={"error": False},
        status_code=HttpCode.BAD_REQUEST.value,
    )

    url = "/create"
    response = test_client.post(
        url, data=json.dumps(correct_payload), headers=json_header
    )

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"error" in response.data


def test_create_transaction_mining_fail(
    test_client, json_header, requests_mock_transaction, correct_payload
):

    requests_mock_transaction.post(
        BisonCoinUrls.mining_url.format("queue"),
        json={"error": "something went wrong"},
        status_code=HttpCode.INTERNAL_SERVER_ERROR.value,
    )

    url = "/create"
    response = test_client.post(
        url, data=json.dumps(correct_payload), headers=json_header
    )

    assert response.status_code == HttpCode.INTERNAL_SERVER_ERROR.value
    assert b"error" in response.data
    assert b"something went wrong" in response.data


def test_create_transaction_correct_payload(
    test_client, json_header, requests_mock_transaction, correct_payload
):

    url = "/create"
    response = test_client.post(
        url, data=json.dumps(correct_payload), headers=json_header
    )

    assert response.json["success"]
    assert response.status_code == HttpCode.CREATED.value
    assert response.json["remaining_amount"] == 0


def test_create_transaction_incorrect_verification(
    test_client, json_header, requests_mock_transaction, correct_payload
):
    correct_payload["id"] = "TestShouldFail"
    url = "/create"

    response = test_client.post(
        url, data=json.dumps(correct_payload), headers=json_header
    )

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert (
        FailureReturnString.SIGNATURE_VERFICATION_FAILURE.value.encode()
        in response.data
    )


def test_create_transaction_public_key_failure(
    test_client, json_header, requests_mock_transaction, correct_payload
):

    requests_mock_transaction.get(
        BisonCoinUrls.user_api_url.format("umnetId/USER1"),
        json={"success": True, "data": {}},
        status_code=HttpCode.BAD_REQUEST.value,
    )

    url = "/create"
    response = test_client.post(
        url, data=json.dumps(correct_payload), headers=json_header
    )

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert FailureReturnString.PUBLIC_KEY_NF.value.encode() in response.data
