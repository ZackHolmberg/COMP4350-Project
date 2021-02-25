import pytest
from src import app
from uuid import uuid4
import json
import sys, os
from ecdsa import SigningKey, VerifyingKey
import base64
from shared import HttpCode, FailureReturnString

if os.environ.get('SERVICE_IN_DOCKER',False):             
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))


@pytest.fixture(scope='module')
def signing_key():
    return SigningKey.generate()

@pytest.fixture(scope='module')
def public_key(signing_key):
    pubk = signing_key.verifying_key.to_string()
    pubk = base64.b64encode(pubk)
    return pubk

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

    assert response.status_code == HttpCode.OK.value
    assert b"Hello Transactions" in response.data


def test_create_transaction_incorrect_payload(test_client, json_header):
    data = {
        'id': '21435',
        'from' : 'user1',
        'to' : 'user2',
        'amount' : 99
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data

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

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data

def test_create_transaction_correct_key_wrong_signature(test_client, json_header, public_key):
    
    data = {
        'id': '21435',
        'from' : public_key.decode(),
        'to' : 'user2',
        'amount' : 99,
        'signature' : 'A wrong signature'
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data

def test_create_transaction_correct_payload(test_client, json_header, signing_key, public_key, requests_mock):
    ## sign a transaction
    to_sign = str(uuid4())
    signature = signing_key.sign(to_sign.encode())
    
    signature = base64.b64encode(signature).decode()

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": True}, status_code=200)

    data = {
        'id' : to_sign,
        'from' : public_key.decode(),
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.CREATED.value
    assert b"success" in response.data
    assert b"true" in response.data
