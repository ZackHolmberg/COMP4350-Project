import pytest
from src import app
import requests
import json
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', '')))

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

    assert response.status_code == HttpCode.OK
    assert b"Hello from your wallet" in response.data

def test_create_wallet_success(test_client, requests_mock):
    url = '/create'

    requests_mock.post("http://localhost/blockchain/wallet/addWallet", json={"success": True})

    response = test_client.post(url, json = {"public_key" : 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.CREATED
    assert json.loads(response.data)["success"] == True


def test_create_wallet_error(test_client, requests_mock):
    url = '/create'

    requests_mock.post("http://localhost/blockchain/wallet/addWallet", json={"error": "wallet ID already exists"}, status_code=400)

    response = test_client.post(url, json = {"public_key" : 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.BAD_REQUEST
    assert json.loads(response.data)["error"] == "wallet ID already exists"


def test_create_wallet_incorrect_payload(test_client, requests_mock):
    url = '/create'

    requests_mock.post("http://localhost/blockchain/wallet/addWallet", json={"error": "wallet ID already exists"}, status_code=400)

    response = test_client.post(url, json = {})

    assert response.status_code == HttpCode.BAD_REQUEST
    assert json.loads(response.data)["error"]== "Please send correct json payload"



def test_get_wallet_amount_success(test_client, requests_mock):
    url = '/amount'

    requests_mock.post("http://localhost/blockchain/wallet/balance", json={"amount":0})

    response = test_client.post(url, json = {"public_key" : 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.OK
    assert json.loads(response.data)["amount"] == 0


def test_get_wallet_amount_error(test_client, requests_mock):
    url = '/amount'

    requests_mock.post("http://localhost/blockchain/wallet/balance", json={"error":"no corresponding wallet for id"}, status_code=400)

    response = test_client.post(url, json = {"public_key" : 'to_be_genetated_elsewhere'})

    assert response.status_code == HttpCode.BAD_REQUEST
    assert json.loads(response.data)["error"] == "no corresponding wallet for id"


def test_get_wallet_amount_incorrect_payload(test_client, requests_mock):
    url = '/amount'

    requests_mock.post("http://localhost/blockchain/wallet/balance", json={"amount":0})

    response = test_client.post(url, json = {})

    assert response.status_code == HttpCode.BAD_REQUEST
    assert json.loads(response.data)["error"]== "Please send correct json payload"