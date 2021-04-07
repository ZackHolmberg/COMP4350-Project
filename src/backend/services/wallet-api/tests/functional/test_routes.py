import json
import os
import sys

import pytest
from src import app

if os.environ.get("SERVICE_IN_DOCKER", False):
    sys.path.append(os.path.abspath(os.path.join("..", "")))
else:
    sys.path.append(os.path.abspath(os.path.join("../..", "")))

from shared import HttpCode


@pytest.fixture(scope="module")
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


def test_home_page(test_client):
    # test GET query on '/' route
    url = "/"

    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert b"Hello from your wallet" in response.data


def test_get_wallet_amount_success(test_client, requests_mock):
    url = "/amount"

    requests_mock.get(
        "http://api-gateway/blockchain/wallet/balance", json={"amount": 0}
    )

    requests_mock.post("http://users:5000/authUser", json={"success": True})

    response = test_client.post(
        url, json={"umnetId": "to_be_genetated_elsewhere", "password": ""}
    )

    assert response.status_code == HttpCode.OK.value
    assert json.loads(response.data)["amount"] == 0


def test_get_wallet_amount_error(test_client, requests_mock):
    url = "/amount"

    requests_mock.get(
        "http://api-gateway/blockchain/wallet/balance",
        json={"error": "no corresponding wallet for id"},
        status_code=400,
    )

    requests_mock.post("http://users:5000/authUser", json={"success": True})

    response = test_client.post(
        url, json={"umnetId": "to_be_genetated_elsewhere", "password": ""}
    )

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert json.loads(response.data)["error"] == "no corresponding wallet for id"


def test_get_wallet_amount_incorrect_payload(test_client, requests_mock):
    url = "/amount"

    requests_mock.post("http://users:5000/authUser", json={"success": True})

    requests_mock.get(
        "http://api-gateway/blockchain/wallet/balance", json={"amount": 0}
    )

    response = test_client.post(url, json={})

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert json.loads(response.data)["error"] == "Please send correct json payload"


def test_transaction_history_successfull_response(test_client, requests_mock):
    url = "/history/SHARMAA2"

    requests_mock.get(
        "http://api-gateway/blockchain/chain",
        json={
            "chain": [
                '{"hash": "0000", "index": 0, "miner_id": "miner_id", "nonce": 0, "prev_hash": "0", "reward_amount": 0, "transaction": {"amount": 0, "from_address": "", "id": "", "signature": "", "timestamp": 0, "to_address": ""}}',
                '{"hash": "0000813999da5fdc0a61293c8b38a91a0b2a1864c3f7b431ed9684b04c53da45", "index": 1, "miner_id": "SACHDEV1", "nonce": 85269, "prev_hash": "0000", "reward_amount": 10, "transaction": {"amount": 2, "from_address": "SACHDEV1", "id": "012d92c16a0841bd4dfd7f8ad071a284e9772ed6f0c755fed4de894f6b0cebf5", "signature": "8b4edeb9b707b958723acdf982afd94ad7bb85ff9f3729f84a72885da517e24832477579f0a464be0531950c16430c4daaaba954d9d2247cc23ba99c3cd5e52a7778282355fb7659867a637fa15301582d7ef5da53bb1bcd687ccf5c671c18ec2123dcc5a48bd937950015efa87ff40486035ca173bb53a1e7314bed52b89ecd", "timestamp": 1616457752, "to_address": "SHARMAA2"}}',
                '{"hash": "00003ff58178aa6383207fc8980530066e2ff3d8e5e91cbebd639615c3561a9d", "index": 2, "miner_id": "SACHDEV1", "nonce": 15368, "prev_hash": "0000813999da5fdc0a61293c8b38a91a0b2a1864c3f7b431ed9684b04c53da45", "reward_amount": 10, "transaction": {"amount": 12, "from_address": "SACHDEV1", "id": "64713990ecb099eaeac7ecaf9fa7559b3fc35c3b7c6008a2328591906b52606d", "signature": "9e9b2bde5b823bbf1fa64b07f241a58d740940eac823960a0c6ecd343b992fdf1b9093d754b850ec8545418cab41badf91e260e25a601a8f19b076ce8dd810b6fe6f38678c1c35d32d9e142d1f820e032912337c844cbe40e8ba524fb4b0dfbe820a99ed4834a6be280917d6f6f2feb746aa7813e706e853eb1ab596bf4ff2a9", "timestamp": 1616457767, "to_address": "SHARMAA2"}}',
                '{"hash": "000095c474acef6e2bfa143a178a0515969775ca597c04a03752049c21da8b09", "index": 3, "miner_id": "SHARMAA2", "nonce": 16310, "prev_hash": "00003ff58178aa6383207fc8980530066e2ff3d8e5e91cbebd639615c3561a9d", "reward_amount": 10, "transaction": {"amount": 3, "from_address": "SACHDEV1", "id": "bf3ca14719becea7a176e0b295d4b6bb9ce1e11461968ff435afe7753d4a4e5c", "signature": "4a9d17230a018d11be53eb65a663199d35fb568f49da69a69c0de13c53e94a17c8aa74d4205f32d5cf361b9eaa9fc781aed9aea59228897c8b624de36630d78ff84837e0f61d7d4850f510d372e6776ea4c32009263cb4b9793c1bb3915f092db27555db4b2cdbce21adcb1d7124cca77e3b2ce3bc0a209e242da152fe5fdf98", "timestamp": 1616457911, "to_address": "SHARMAA2"}}',
            ],
            "length": 4,
        },
        status_code=200,
    )

    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert (
        b'"history":[{"transaction":{"amount":3,"from_address":"SACHDEV1","id":"bf3ca14719becea7a176e0b295d4b6bb9ce1e11461968ff435afe7753d4a4e5c","signature":"4a9d17230a018d11be53eb65a663199d35fb568f49da69a69c0de13c53e94a17c8aa74d4205f32d5cf361b9eaa9fc781aed9aea59228897c8b624de36630d78ff84837e0f61d7d4850f510d372e6776ea4c32009263cb4b9793c1bb3915f092db27555db4b2cdbce21adcb1d7124cca77e3b2ce3bc0a209e242da152fe5fdf98","timestamp":1616457911,"to_address":"SHARMAA2"},"type":"receive"},{"transaction":{"amount":10,"from_address":"BLOCKCHAIN","id":"bf3ca14719becea7a176e0b295d4b6bb9ce1e11461968ff435afe7753d4a4e5c","signature":"4a9d17230a018d11be53eb65a663199d35fb568f49da69a69c0de13c53e94a17c8aa74d4205f32d5cf361b9eaa9fc781aed9aea59228897c8b624de36630d78ff84837e0f61d7d4850f510d372e6776ea4c32009263cb4b9793c1bb3915f092db27555db4b2cdbce21adcb1d7124cca77e3b2ce3bc0a209e242da152fe5fdf98","timestamp":1616457911,"to_adderss":"SHARMAA2"},"type":"reward"}'
        in response.data
    )


def test_transaction_history_success_empty_response(test_client, requests_mock):
    url = "/history/DoesntExist"

    requests_mock.get(
        "http://api-gateway/blockchain/chain",
        json={
            "chain": [
                '{"hash": "0000", "index": 0, "miner_id": "miner_id", "nonce": 0, "prev_hash": "0", "reward_amount": 0, "transaction": {"amount": 0, "from_address": "", "id": "", "signature": "", "timestamp": 0, "to_address": ""}}',
                '{"hash": "0000813999da5fdc0a61293c8b38a91a0b2a1864c3f7b431ed9684b04c53da45", "index": 1, "miner_id": "SACHDEV1", "nonce": 85269, "prev_hash": "0000", "reward_amount": 10, "transaction": {"amount": 2, "from_address": "SACHDEV1", "id": "012d92c16a0841bd4dfd7f8ad071a284e9772ed6f0c755fed4de894f6b0cebf5", "signature": "8b4edeb9b707b958723acdf982afd94ad7bb85ff9f3729f84a72885da517e24832477579f0a464be0531950c16430c4daaaba954d9d2247cc23ba99c3cd5e52a7778282355fb7659867a637fa15301582d7ef5da53bb1bcd687ccf5c671c18ec2123dcc5a48bd937950015efa87ff40486035ca173bb53a1e7314bed52b89ecd", "timestamp": 1616457752, "to_address": "SHARMAA2"}}',
                '{"hash": "00003ff58178aa6383207fc8980530066e2ff3d8e5e91cbebd639615c3561a9d", "index": 2, "miner_id": "SACHDEV1", "nonce": 15368, "prev_hash": "0000813999da5fdc0a61293c8b38a91a0b2a1864c3f7b431ed9684b04c53da45", "reward_amount": 10, "transaction": {"amount": 12, "from_address": "SACHDEV1", "id": "64713990ecb099eaeac7ecaf9fa7559b3fc35c3b7c6008a2328591906b52606d", "signature": "9e9b2bde5b823bbf1fa64b07f241a58d740940eac823960a0c6ecd343b992fdf1b9093d754b850ec8545418cab41badf91e260e25a601a8f19b076ce8dd810b6fe6f38678c1c35d32d9e142d1f820e032912337c844cbe40e8ba524fb4b0dfbe820a99ed4834a6be280917d6f6f2feb746aa7813e706e853eb1ab596bf4ff2a9", "timestamp": 1616457767, "to_address": "SHARMAA2"}}',
                '{"hash": "000095c474acef6e2bfa143a178a0515969775ca597c04a03752049c21da8b09", "index": 3, "miner_id": "SHARMAA2", "nonce": 16310, "prev_hash": "00003ff58178aa6383207fc8980530066e2ff3d8e5e91cbebd639615c3561a9d", "reward_amount": 10, "transaction": {"amount": 3, "from_address": "SACHDEV1", "id": "bf3ca14719becea7a176e0b295d4b6bb9ce1e11461968ff435afe7753d4a4e5c", "signature": "4a9d17230a018d11be53eb65a663199d35fb568f49da69a69c0de13c53e94a17c8aa74d4205f32d5cf361b9eaa9fc781aed9aea59228897c8b624de36630d78ff84837e0f61d7d4850f510d372e6776ea4c32009263cb4b9793c1bb3915f092db27555db4b2cdbce21adcb1d7124cca77e3b2ce3bc0a209e242da152fe5fdf98", "timestamp": 1616457911, "to_address": "SHARMAA2"}}',
            ],
            "length": 4,
        },
        status_code=200,
    )

    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert response.get_json()["history"] == []


def test_get_wallet_amount_auth_failure(test_client, requests_mock):
    url = "/amount"

    requests_mock.post(
        "http://users:5000/authUser", json={"error": "Some failure in auth"}
    )

    requests_mock.get(
        "http://api-gateway/blockchain/wallet/balance", json={"amount": 0}
    )

    response = test_client.post(
        url, json={"umnetId": "um", "password": "wrong_password"}
    )

    assert b"Some failure in auth" in response.data
