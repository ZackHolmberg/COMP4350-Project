import pytest
from src import app
from uuid import uuid4
import json
import sys, os

from shared import HttpCode, FailureReturnString

if os.environ.get('SERVICE_IN_DOCKER',False):             
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

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

def test_create_transaction_wrong_wallet_amount(test_client, json_header, requests_mock):
    data = {
        'from' : 'user1',
        'to' : 'user2',
        'amount' : 99,
    }
    url = '/create'

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": False}, status_code=400)

    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.BAD_REQUEST.value
    assert b"err" in response.data
    assert b"Unable" in response.data


def test_create_transaction_mining_fail(test_client, json_header, requests_mock):
    
    data = {
        'from' : "user1",
        'to' : 'user2',
        'amount' : 99,
    }
    url = '/create'

    requests_mock.post("http://mining:5000/queue",
                       json={"err": "something went wrong"}, status_code=500)


    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.INTERNAL_SERVER_ERROR.value
    assert b"err" in response.data

def test_create_transaction_correct_payload(test_client, json_header, requests_mock):

    requests_mock.post("http://blockchain:5000/wallet/verifyAmount",
                       json={"valid": True}, status_code=200)

    requests_mock.post("http://mining:5000/queue",
                       json={"success": True}, status_code=201)
    data = {
        'from' : "user1",
        'to' : 'user2',
        'amount' : 99,
    }

    url = '/create'


    response = test_client.post(url, data=json.dumps(data), headers=json_header)

    assert response.status_code == HttpCode.CREATED.value
    assert b"success" in response.data
    assert b"true" in response.data
