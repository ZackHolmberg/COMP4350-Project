import pytest
from src import app
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


@pytest.fixture(scope='module')
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


def test_get_chain(test_client):
    # test GET query on '/' route
    url = '/chain'
    response = test_client.get(url)
    data = json.loads(response.json['chain'][0])
    assert response.status_code == 200
    assert response.json['length'] == 1
    assert data['hash'] == "0000"
    assert data['index'] == 0
    assert data['nonce'] == 0
    assert data['prev_hash'] == "0"
    assert data['transaction'] == {"amount": 0,
                                   "from_address": "", "to_address": ""}


def test_add_wallet(test_client):
    url = '/wallet/addWallet'
    data = {'walletId': "fake_wallet_id"}

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    assert response.json['success'] == True

    response = test_client.post(url, data=json.dumps(data), headers=headers)

    assert response.status_code == 400
    assert response.json['err'] == "wallet ID already exists"


def test_verify_amount(test_client):
    url = '/wallet/verifyAmount'
    data1 = {'walletId': "fake_wallet_id",
             'amount': 0}
    data2 = {'walletId': "fake_wallet_id",
             'amount': 5}

    response = test_client.post(url, data=json.dumps(data1), headers=headers)

    assert response.status_code == 200
    assert response.json['valid'] == True

    response = test_client.post(url, data=json.dumps(data2), headers=headers)

    assert response.status_code == 200
    assert response.json['valid'] == False


def test_get_wallet_amount(test_client):
    url = '/wallet/balance'
    data1 = {'walletId': "fake_wallet_id"}
    data2 = {'walletId': "non_existent_wallet_id"}

    response = test_client.post(url, data=json.dumps(data1), headers=headers)

    assert response.status_code == 200
    assert response.json['amount'] == 0

    response = test_client.post(url, data=json.dumps(data2), headers=headers)

    assert response.status_code == 400
    assert response.json['err'] == "no corresponding wallet for id"
