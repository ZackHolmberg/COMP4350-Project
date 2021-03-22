import pytest
from src import app
import json
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode

@pytest.fixture(scope='module')
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


def test_home_page(test_client):
    # test GET query on '/' route
    url = '/'

    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert b"Hello from your wallet" in response.data


def test_create_wallet_success(test_client, requests_mock):
    url = '/create'

    requests_mock.post(
        "http://blockchain:5000/wallet/addWallet", json={"success": True}, status_code=201)

    response = test_client.post(
        url, json={"walletId": 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.CREATED.value
    assert json.loads(response.data)["success"] == True


def test_create_wallet_error(test_client, requests_mock):
    url = '/create'

    requests_mock.post("http://blockchain:5000/wallet/addWallet",
                       json={"error": "wallet ID already exists"}, status_code=400)

    response = test_client.post(
        url, json={"walletId": 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert json.loads(response.data)["error"] == "wallet ID already exists"


def test_create_wallet_incorrect_payload(test_client, requests_mock):
    url = '/create'

    requests_mock.post("http://blockchain:5000/wallet/addWallet",
                       json={"error": "wallet ID already exists"}, status_code=400)

    response = test_client.post(url, json={})

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert json.loads(response.data)[
        "error"] == "Please send correct json payload"


def test_get_wallet_amount_success(test_client, requests_mock):
    url = '/amount'

    requests_mock.get(
        "http://blockchain:5000/wallet/balance", json={"amount": 0})

    response = test_client.post(
        url, json={"walletId": 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.OK.value
    assert json.loads(response.data)["amount"] == 0


def test_get_wallet_amount_error(test_client, requests_mock):
    url = '/amount'

    requests_mock.get("http://blockchain:5000/wallet/balance",
                       json={"error": "no corresponding wallet for id"}, status_code=400)

    response = test_client.post(
        url, json={"walletId": 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert json.loads(response.data)[
        "error"] == "no corresponding wallet for id"


def test_get_wallet_amount_incorrect_payload(test_client, requests_mock):
    url = '/amount'

    requests_mock.post(
        "http://blockchain:5000/wallet/balance", json={"amount": 0})

    response = test_client.post(url, json={})

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert json.loads(response.data)[
        "error"] == "Please send correct json payload"

def test_transaction_history_incorrect_payload(test_client, requests_mock):
    url = '/history'

    requests_mock.get("http://blockchain:5000/chain",
        json={"chain": [
            "{\"hash\": \"0000\", \"index\": 0, \"miner_id\": \"miner_id\", \"nonce\": 0, \"prev_hash\": \"0\", \"reward_amount\": 0, \"timestamp\": \"1616379961.166997\", \"transaction\": {\"amount\": 0, \"from_address\": \"\", \"to_address\": \"\"}}",
            "{\"hash\": \"0000e1e01b27d6fad766167a766769b86b70ab4db68893e4e7b754ec7166a714\", \"index\": 1, \"miner_id\": \"SHARMAA2\", \"nonce\": 310, \"prev_hash\": \"0000\", \"reward_amount\": 10, \"timestamp\": \"1616380435.8265228\", \"transaction\": {\"amount\": 2, \"from_address\": \"SACHDEV1\", \"to_address\": \"FINESM1\"}}",
            "{\"hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"index\": 2, \"miner_id\": \"HOLMBERGZ1\", \"nonce\": 18761, \"prev_hash\": \"0000e1e01b27d6fad766167a766769b86b70ab4db68893e4e7b754ec7166a714\", \"reward_amount\": 10, \"timestamp\": \"1616380614.211374\", \"transaction\": {\"amount\": 2, \"from_address\": \"FINESM1\", \"to_address\": \"SHARMAA2\"}}",
            "{\"hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"index\": 3, \"miner_id\": \"SACHDEV1\", \"nonce\": 18761, \"prev_hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"reward_amount\": 10, \"timestamp\": \"1616380626.2039511\", \"transaction\": {\"amount\": 2, \"from_address\": \"SHARMAA2\", \"to_address\": \"HOLMBERGZ1\"}}"
        ],
        "length": 4}, status_code=200)
    
    response = test_client.get(url)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b'Please send correct json payload' in response.data

def test_transaction_history_success_full_response(test_client, requests_mock):
    url = '/history?walletId=SHARMAA2'

    requests_mock.get("http://blockchain:5000/chain",
        json={"chain": [
            "{\"hash\": \"0000\", \"index\": 0, \"miner_id\": \"miner_id\", \"nonce\": 0, \"prev_hash\": \"0\", \"reward_amount\": 0, \"timestamp\": \"1616379961.166997\", \"transaction\": {\"amount\": 0, \"from_address\": \"\", \"to_address\": \"\"}}",
            "{\"hash\": \"0000e1e01b27d6fad766167a766769b86b70ab4db68893e4e7b754ec7166a714\", \"index\": 1, \"miner_id\": \"SHARMAA2\", \"nonce\": 310, \"prev_hash\": \"0000\", \"reward_amount\": 10, \"timestamp\": \"1616380435.8265228\", \"transaction\": {\"amount\": 2, \"from_address\": \"SACHDEV1\", \"to_address\": \"FINESM1\"}}",
            "{\"hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"index\": 2, \"miner_id\": \"HOLMBERGZ1\", \"nonce\": 18761, \"prev_hash\": \"0000e1e01b27d6fad766167a766769b86b70ab4db68893e4e7b754ec7166a714\", \"reward_amount\": 10, \"timestamp\": \"1616380614.211374\", \"transaction\": {\"amount\": 2, \"from_address\": \"FINESM1\", \"to_address\": \"SHARMAA2\"}}",
            "{\"hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"index\": 3, \"miner_id\": \"SACHDEV1\", \"nonce\": 18761, \"prev_hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"reward_amount\": 10, \"timestamp\": \"1616380626.2039511\", \"transaction\": {\"amount\": 2, \"from_address\": \"SHARMAA2\", \"to_address\": \"HOLMBERGZ1\"}}"
        ],
        "length": 4}, status_code=200)
    
    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert b'"history":[{"Timestamp":1616380626.2039511,"amount":2,"to":"HOLMBERGZ1"},{"Timestamp":1616380614.211374,"amount":2,"from":"FINESM1"},{"Timestamp":1616380435.8265228,"amount":10,"from":"Mining"}]' in response.data

def test_transaction_history_success_empty_response(test_client, requests_mock):
    url = '/history?walletId=DoesntExist'

    requests_mock.get("http://blockchain:5000/chain",
        json={"chain": [
            "{\"hash\": \"0000\", \"index\": 0, \"miner_id\": \"miner_id\", \"nonce\": 0, \"prev_hash\": \"0\", \"reward_amount\": 0, \"timestamp\": \"1616379961.166997\", \"transaction\": {\"amount\": 0, \"from_address\": \"\", \"to_address\": \"\"}}",
            "{\"hash\": \"0000e1e01b27d6fad766167a766769b86b70ab4db68893e4e7b754ec7166a714\", \"index\": 1, \"miner_id\": \"SHARMAA2\", \"nonce\": 310, \"prev_hash\": \"0000\", \"reward_amount\": 10, \"timestamp\": \"1616380435.8265228\", \"transaction\": {\"amount\": 2, \"from_address\": \"SACHDEV1\", \"to_address\": \"FINESM1\"}}",
            "{\"hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"index\": 2, \"miner_id\": \"HOLMBERGZ1\", \"nonce\": 18761, \"prev_hash\": \"0000e1e01b27d6fad766167a766769b86b70ab4db68893e4e7b754ec7166a714\", \"reward_amount\": 10, \"timestamp\": \"1616380614.211374\", \"transaction\": {\"amount\": 2, \"from_address\": \"FINESM1\", \"to_address\": \"SHARMAA2\"}}",
            "{\"hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"index\": 3, \"miner_id\": \"SACHDEV1\", \"nonce\": 18761, \"prev_hash\": \"000037a1d5bd16f2f85a2fc13eea74a761db2b154d1e64df0dff810cb6a3f427\", \"reward_amount\": 10, \"timestamp\": \"1616380626.2039511\", \"transaction\": {\"amount\": 2, \"from_address\": \"SHARMAA2\", \"to_address\": \"HOLMBERGZ1\"}}"
        ],
        "length": 4}, status_code=200)
    
    response = test_client.get(url)

    assert response.status_code == HttpCode.OK.value
    assert response.get_json()["history"] == []
