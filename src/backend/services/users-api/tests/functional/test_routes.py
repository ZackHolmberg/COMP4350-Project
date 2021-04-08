import pytest
from unittest.mock import patch
from src.databases import database_init
import mongomock
import json
from werkzeug.security import check_password_hash, generate_password_hash

with patch.object(database_init, 'create_users_db', return_value=mongomock.MongoClient()):
    from src.app import app
    from src.app import mongo

import sys
import os


sys.path.append(os.path.abspath(os.path.join('..', '')))

from shared import FailureReturnString

user_one_pass = "akshay123"
user_two_pass = "abhi123"
user_one = {"first_name": "Akshay", "last_name": "Sharma",
            "umnetId": "SHARMAA2", "password": generate_password_hash(user_one_pass, method="sha256"), "public_key": "akshay_pk"}
user_two = {"first_name": "Abhi", "last_name": "Sachdev",
            "umnetId": "SACHDEV1", "password": generate_password_hash(user_two_pass, method="sha256"), "public_key": "abhi_pk"}

@pytest.fixture(scope='module')
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


@pytest.fixture(scope='module')
def test_db_patch():
    mongo.db.create_collection("users")
    mongo.db.users.insert_one(user_one)
    mongo.db.users.insert_one(user_two)
    mongo.db.users.create_index("umnetId", unique=True)
    mongo.db.users.create_index("public_key", unique=True)


@pytest.fixture(scope='module')
def json_header():

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    return headers

@pytest.fixture(scope='function')
def requests_mock_users(requests_mock):
    requests_mock.post("http://api-gateway/blockchain/wallet/addWallet",
        json={"success": True}, status_code=200)
    return requests_mock

@pytest.fixture(scope='module')
def test_payload():
    payload = {
        "first_name": "Madison",
        "last_name": "Fines",
        "umnetId": "FINESM1",
        "password": "madison123",
        "public_key": "madison_pk"
    }
    return payload


@pytest.fixture(scope='module')
def update_user_payload():    
    payload = {
        "first_name": user_one['first_name'],
        "last_name": user_one['last_name'],
        "umnetId": user_one['umnetId'],
        "curr_password": user_one_pass,
        "new_password": "akshay234"
    }

    return payload

@pytest.fixture(scope='module')
def login_payload(test_payload):
    payload = {
        "umnetId": test_payload['umnetId'],
        "password": test_payload['password'],
    }
    return payload

def test_home_page(test_client, test_db_patch):
    # test GET query on '/' route
    url = '/'
    response = test_client.get(url)

    assert response.status_code == 200
    resp_msg = "Hello Users of " + mongo.db.name
    assert resp_msg.encode('utf-8') in response.data


def test_create_user(test_client, json_header, requests_mock_users, test_payload):
    url = '/create'

    response = test_client.post(
        url, data=json.dumps(test_payload), headers=json_header)
    assert response.json['success']
    user = mongo.db.users.find_one({"umnetId": test_payload["umnetId"]})
    assert user is not None


def test_login_success(test_client, json_header, test_payload, login_payload):
    url = '/login'

    expected_return = {
        "first_name": test_payload['first_name'],
        "last_name": test_payload['last_name'],
        "public_key": test_payload['public_key']
    }

    response = test_client.post(
        url, data=json.dumps(login_payload), headers=json_header)
    assert response.json['user'] == expected_return


def test_login_user_wrong_pass(test_client, json_header, login_payload):
    url = '/login'
    login_payload['password'] = 'SomethingObviouslyWrong'

    response = test_client.post(
        url, data=json.dumps(login_payload), headers=json_header)
    assert response.json['error'] == FailureReturnString.INCORRECT_CREDENTIALS.value


def test_login_user_not_in_db(test_client, json_header, login_payload):

    # remove the added user to cause unsuccessful login
    mongo.db.users.delete_one({"umnetId": login_payload["umnetId"]})

    url = '/login'
    response = test_client.post(
        url, data=json.dumps(login_payload), headers=json_header)
    assert response.json['error'] == FailureReturnString.INCORRECT_CREDENTIALS.value


def test_get_all_users(test_client, test_db_patch):
    url = '/list'

    response = test_client.get(url) 
    assert user_one['umnetId'].encode() in response.data
    assert user_two['umnetId'].encode() in response.data
    assert b'"umnetId":"FINESM1"' not in response.data
    

def test_create_error_duplicate_umnetId_and_password(test_client, test_db_patch, test_payload, json_header):

    url = '/create'

    # duplicate umnetId
    test_payload['umnetId'] = user_one['umnetId']

    response = test_client.post(
        url, data=json.dumps(test_payload), headers=json_header)

    assert FailureReturnString.DATABASE_VERIFICATION_FAILURE.value.encode() in response.data

    # duplicate public key
    payload = {
        "first_name": "Bob",
        "last_name": "Dylan",
        "umnetId": "DYLANB1",
        "password": "bob123",
        "public_key": user_one['public_key']
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    assert FailureReturnString.DATABASE_VERIFICATION_FAILURE.value.encode() in response.data


def test_create_error_incomplete_payload(test_client, test_db_patch, json_header, test_payload):
    url = '/create'
    del test_payload['first_name']
    response = test_client.post(
        url, data=json.dumps(test_payload), headers=json_header)

    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data


def test_success_get_user_by_umnetId(test_client, test_db_patch):
    url = '/umnetId/' + user_one['umnetId']
    response = test_client.get(url)
    assert user_one['umnetId'].encode() in response.data


def test_failure_get_user_by_umnetId_user_not_found(test_client, test_db_patch):
    url = '/umnetId/DOESNTEXIST'
    response = test_client.get(url)
    assert response.json['error'] == FailureReturnString.USER_NOT_FOUND.value


def test_success_update_user(test_client, test_db_patch, json_header, update_user_payload):
    url = '/update'

    response = test_client.post(
        url, data=json.dumps(update_user_payload), headers=json_header)
    # Check the response to see if its correct
    assert response.json['success']

    # Check the db to see if the updates were successful
    db_user = mongo.db.users.find_one({"umnetId": update_user_payload["umnetId"]})
    assert check_password_hash(db_user["password"], update_user_payload["new_password"])

    new_password = update_user_payload['new_password']
    update_user_payload['new_password'] = update_user_payload['curr_password']
    
    response = test_client.post(
        url, data=json.dumps(update_user_payload), headers=json_header)
    
    # Check if the pw in database is still correct
    db_user = mongo.db.users.find_one({"umnetId": update_user_payload['umnetId']})
    assert check_password_hash(db_user["password"], new_password)
    # Check if the response is correct
    assert FailureReturnString.INCORRECT_CREDENTIALS.value.encode() in response.data

    # change the password back to original (bonus test lol)
    update_user_payload["curr_password"] = new_password
    update_user_payload["new_password"] = user_one_pass

    response = test_client.post(
        url, data=json.dumps(update_user_payload), headers=json_header)

    # Check if the response is correct
    assert response.json['success']

    # Check if the database was updated successfully
    db_user = mongo.db.users.find_one({"umnetId": update_user_payload["umnetId"]})
    assert check_password_hash(db_user["password"], update_user_payload["new_password"])
    

def test_failure_update_user_user_not_found(test_client, test_db_patch, json_header):
    url = '/update'

    payload = {
        "first_name": "Fake",
        "last_name": "User",
        "umnetId": "DOES_NOT_EXIST",
        "curr_password": "fake123",
        "new_password": "fake123",
        "public_key": "fake_pk"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    assert FailureReturnString.INCORRECT_CREDENTIALS.value.encode() in response.data

def test_failure_update_user_incomplete_payload(test_client, test_db_patch, json_header, test_payload):
    url = '/update'

    response = test_client.post(
        url, data=json.dumps(test_payload), headers=json_header)

    assert FailureReturnString.INCORRECT_PAYLOAD.value.encode() in response.data

def test_auth_user(test_client, json_header, requests_mock):

    url = '/authUser'

    payload = {
        "umnetId": user_one['umnetId'],
        "password": user_one_pass,
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert response.json['success']

def test_auth_user_password_incorrect(test_client, json_header, requests_mock):

    url = '/authUser'

    payload = {
        "umnetId": user_one['umnetId'],
        "password": "akshay234567",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert FailureReturnString.INCORRECT_CREDENTIALS.value.encode() in response.data

def test_auth_user_umnetid_incorrect(test_client, json_header, requests_mock):

    url = '/authUser'

    payload = {
        "umnetId": "SHARMAA3",
        "password": "akshay123",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert FailureReturnString.INCORRECT_CREDENTIALS.value.encode() in response.data
