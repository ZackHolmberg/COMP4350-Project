import pytest
from src import app
from uuid import uuid4
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

@pytest.fixture(scope='module')
def json_header():

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    return headers

def test_home_page(test_client):
    # test GET query on '/' route
    url = '/'

    response = test_client.get(url)

    assert response.status_code == HttpCode.OK
    assert b"Hello Transactions" in response.data

def test_sign_incorrect_payload(test_client, json_header):
    data = {
        'Data': [20.0, 30.0, 401.0, 50.0]
    }
    url = '/sign'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"Exception" in response.data


def test_sign_no_user(test_client, json_header):
    data = {
        'to_sign' : str(uuid4()),
        'user' : "shalala"
    }

    url = '/sign'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"Exception" in response.data
    assert b"json payload" in response.data

def test_keygen_no_user(test_client, json_header):
    data = {
    }

    url = '/keygen'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"false" in response.data

def test_keygen_correct(test_client, json_header):
    data = {
        'user': "test"
    }

    url = '/keygen'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.CREATED
    assert b"success" in response.data
    assert b"true" in response.data


def test_sign_user_present(test_client, json_header):
    data = {
        'user': "signTest"
    }

    url = '/keygen'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)
    
    data = {
        'to_sign' : str(uuid4()),
        'user' : "signTest"
    }
    url = '/sign'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.OK
    assert b"to_sign" in response.data
    assert b"signature" in response.data


def test_address_no_user(test_client, json_header):
    url = '/address/notpresent'

    response = test_client.get(url)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"Exception" in response.data
    assert b"json payload" in response.data

def test_address_correct_payload(test_client, json_header):
    data = {
        'user': "addressTest"
    }

    url = '/keygen'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    url = '/address/addressTest'

    response = test_client.get(url)

    assert response.status_code == HttpCode.OK
    assert b"address" in response.data 


def test_address_incorrect_payload(test_client, json_header):
    url = '/address'

    response = test_client.get(url)

    assert response.status_code == HttpCode.NOT_FOUND


def test_create_transaction_incorrect_payload(test_client, json_header):
    data = {
        'id': '21435',
        'from' : 'user1',
        'to' : 'user2',
        'amount' : 99
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"Exception" in response.data
    assert b"json payload" in response.data

def test_create_transaction_wrong_key(test_client, json_header):
    data = {
        'id': '21435',
        'from' : 'user1',
        'to' : 'user2',
        'amount' : 99,
        'signature' : 'A wrong signature'
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"Exception" in response.data

def test_create_transaction_correct_key_wrong_signature(test_client, json_header):
    data = {
        'user': "transactionTest"
    }

    url = '/keygen'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    url = '/address/transactionTest'

    response = test_client.get(url)
    
    address_from = response.get_json()["address"]

    data = {
        'id': '21435',
        'from' : address_from,
        'to' : 'user2',
        'amount' : 99,
        'signature' : 'A wrong signature'
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST
    assert b"Exception" in response.data

def test_create_transaction_correct_key_wrong_signature(test_client, json_header):
    ## add user with the key
    data = {
        'user': "transactionTest"
    }

    url = '/keygen'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    url = '/address/transactionTest'

    response = test_client.get(url)
    
    address_from = response.get_json()["address"]

    ## sign a transaction
    to_sign = str(uuid4())
    data = {
        'to_sign' : to_sign,
        'user' : "transactionTest"
    }

    url = '/sign'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    signature = response.get_json()["signature"]
    print(signature)
    print(address_from)
    data = {
        'id': to_sign,
        'from' : address_from,
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    print(response.data)

    assert response.status_code == HttpCode.CREATED
    assert b"success" in response.data
    assert b"true" in response.data
