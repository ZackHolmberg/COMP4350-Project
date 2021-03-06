import pytest
from src import app
import json
import sys, os
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import codecs
from Crypto.Random import get_random_bytes

from shared import HttpCode, FailureReturnString

if os.environ.get('SERVICE_IN_DOCKER',False):             
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

@pytest.fixture(scope='module')
def key():
    key = RSA.generate(bits=1024, randfunc=get_random_bytes)
    return key

@pytest.fixture(scope='module')
def signing_key(key):
    private_key = key.exportKey()
    return RSA.import_key(private_key)

@pytest.fixture(scope='module')
def public_key(key):
    public_key = key.public_key().exportKey()
    return public_key.decode()

@pytest.fixture(scope='module')
def transaction_id():
    return SHA256.new(str.encode("Test"))

@pytest.fixture(scope='module')
def signature(transaction_id, signing_key):
    signer = PKCS1_v1_5.new(signing_key)
    signature = signer.sign(transaction_id)
    hexify = codecs.getencoder('hex')
    return hexify(signature)[0].decode()

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
        'from' : 'user1',
        'to' : 'user2',
    }
    url = '/create'

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data

def test_create_transaction_wrong_wallet_amount(test_client, json_header, requests_mock, public_key, signature):
    
    data = {
        'id' : "Test",
        'from' : public_key,
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }
    url = '/create'

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": False}, status_code=400)

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert b"Unable" in response.data


def test_create_transaction_mining_fail(test_client, json_header, requests_mock, public_key, signature):
    
    data = {
        'id' : "Test",
        'from' : public_key,
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }

    url = '/create'

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://blockchain:5000/wallet/checkWallet",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://mining:5000/queue",
                       json={"err": "something went wrong"}, status_code=500)


    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.INTERNAL_SERVER_ERROR.value
    assert b"err" in response.data
    assert b"something went wrong" in response.data

def test_create_transaction_correct_payload(test_client, json_header, requests_mock, signature, public_key):

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://blockchain:5000/wallet/checkWallet",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://mining:5000/queue",
                       json={"success": True}, status_code=201)
    data = {
        'id' : "Test",
        'from' : public_key,
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }

    url = '/create'


    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.CREATED.value
    assert b"success" in response.data
    assert b"true" in response.data

def test_create_transaction_incorrect_verification(test_client, json_header, requests_mock, signature, public_key):

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://mining:5000/queue",
                       json={"success": True}, status_code=201)
    data = {
        'id' : "TestSomethingElse",
        'from' : public_key,
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }

    url = '/create'


    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert b"verification" in response.data


def test_create_transaction_receiver_verification_failure(test_client, json_header, requests_mock, signature, public_key):

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://blockchain:5000/wallet/checkWallet",
                       json={"valid": True}, status_code=500)

    requests_mock.post("http://mining:5000/queue",
                       json={"success": True}, status_code=201)
    data = {
        'id' : "TestSomethingElse",
        'from' : public_key,
        'to' : 'user2',
        'amount' : 99,
        'signature' : signature
    }

    url = '/create'


    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
