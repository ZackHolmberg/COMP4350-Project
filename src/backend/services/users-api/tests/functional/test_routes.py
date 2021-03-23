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


if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import FailureReturnString


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

    mongo.db.users.insert_one({"first_name": "Akshay", "last_name": "Sharma",
                               "umnetId": "SHARMAA2", "password": generate_password_hash("akshay123", method="sha256"), "public_key": "akshay_pk"})
    mongo.db.users.insert_one({"first_name": "Abhi", "last_name": "Sachdev",
                               "umnetId": "SACHDEV1", "password": generate_password_hash("abhi123", method="sha256"), "public_key": "abhi_pk"})
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


def test_home_page(test_client, test_db_patch):
    # test GET query on '/' route

    url = '/'

    response = test_client.get(url)

    assert response.status_code == 200
    resp_msg = "Hello Users of " + mongo.db.name
    assert resp_msg.encode('utf-8') in response.data


def test_create_user(test_client, json_header, requests_mock):
    requests_mock.post("http://blockchain:5000/wallet/addWallet",
                json={"success": True}, status_code=200)

    url = '/create'

    payload = {
        "first_name": "Madison",
        "last_name": "Fines",
        "umnetId": "FINESM1",
        "password": "madison123",
        "public_key": "madison_pk"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert response.json['success'] == True
    user = mongo.db.users.find_one({"umnetId": "FINESM1"})
    assert user is not None


def test_login_success(test_client, json_header):
    url = '/login'

    payload = {
        "umnetId": "FINESM1",
        "password": "madison123",
    }

    expected_return = {
        "first_name": "Madison",
        "last_name": "Fines",
        "public_key": "madison_pk"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert response.json['user'] == expected_return


def test_login_user_not_in_db(test_client, json_header):
    url = '/login'

    payload = {
        "umnetId": "FINESM1",
        "password": "wrongPassword",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert response.json['error'] == FailureReturnString.INCORRECT_CREDENTIALS.value


def test_login_user_not_in_db(test_client, json_header):

    # remove the added user to cause unsuccessful login
    mongo.db.users.delete_one({"umnetId": "FINESM1"})

    url = '/login'

    payload = {
        "umnetId": "FINESM1",
        "password": "madison123",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert response.json['error'] == FailureReturnString.INCORRECT_CREDENTIALS.value


def test_get_all_users(test_client, test_db_patch):

    url = '/list'

    response = test_client.get(url)

    assert b'"umnetId":"SHARMAA2"' in response.data
    assert b'"umnetId":"SACHDEV1"' in response.data


def test_create_error_duplicate_umnetId_and_password(test_client, test_db_patch, json_header):

    url = '/create'

    # duplicate umnetId
    payload = {
        "first_name": "Zack",
        "last_name": "Holmberg",
        "umnetId": "SHARMAA2",
        "password": "zack123",
        "public_key": "zack_pk"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    assert b"Database validation failed! Please check your input and try again." in response.data

    # duplicate private key
    payload = {
        "first_name": "Bob",
        "last_name": "Dylan",
        "umnetId": "DYLANB1",
        "password": "bob123",
        "public_key": "abhi_pk"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    assert b"Database validation failed! Please check your input and try again." in response.data


def test_create_error_incomplete_payload(test_client, test_db_patch, json_header):
    url = '/create'

    # duplicate umnetId
    payload = {
        "first_name": "Bob",
        "last_name": "Dylan",
        "umnetId": "SHARMAA2",
        "password": "bob123"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    assert b'Please send correct json payload' in response.data


def test_success_get_user_by_umnetId(test_client, test_db_patch):
    url = '/umnetId/SHARMAA2'

    response = test_client.get(url)

    assert b'"umnetId":"SHARMAA2"' in response.data


def test_failure_get_user_by_umnetId_user_not_found(test_client, test_db_patch):
    url = '/umnetId/DOESNTEXIST'

    response = test_client.get(url)

    assert response.json['error'] == FailureReturnString.USER_NOT_FOUND.value


def test_success_update_user(test_client, test_db_patch, json_header):
    url = '/update'

    payload = {
        "first_name": "Akshay",
        "last_name": "Sharma",
        "umnetId": "SHARMAA2",
        "curr_password": "akshay123",
        "new_password": "akshay234",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    # Check the response to see if its correct
    assert response.json['success'] == True

    # Check the db to see if the updates were successful
    db_user = mongo.db.users.find_one({"umnetId": "SHARMAA2"})
    assert check_password_hash(db_user["password"], "akshay234")

    # Try changing it back with wrong password
    # Check the response to see if it's correct
    assert response.json['success'] == True

    # change the password back to original (bonus test lol)
    payload = {
        "first_name": "Akshay",
        "last_name": "Sharma",
        "umnetId": "SHARMAA2",
        "curr_password": "akshay123",
        "new_password": "akshay123",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    
    # Check if the pw in database is still correct
    db_user = mongo.db.users.find_one({"umnetId": "SHARMAA2"})
    assert check_password_hash(db_user["password"], "akshay234")
    # Check if the response is correct
    assert b'"Incorrect umnetId or password"' in response.data
    

    # change the password back to original (bonus test lol)
    payload = {
        "first_name": "Akshay",
        "last_name": "Sharma",
        "umnetId": "SHARMAA2",
        "curr_password": "akshay234",
        "new_password": "akshay123",
        "public_key": "akshay_pk"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    # Check if the response is correct
    assert response.json['success'] == True

    # Check if the database was updated successfully
    db_user = mongo.db.users.find_one({"umnetId": "SHARMAA2"})
    assert check_password_hash(db_user["password"], "akshay123")


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

    assert b"Incorrect umnetId or password" in response.data

def test_failure_update_user_incomplete_payload(test_client, test_db_patch, json_header):
    url = '/update'

    # payload with missing public key
    payload = {
        "first_name": "Akshay",
        "last_name": "Sharma",
        "umnetId": "SHARMAA2",
        "password": "akshay123"
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)

    assert b'Please send correct json payload' in response.data

def test_auth_user(test_client, json_header, requests_mock):

    url = '/authUser'

    payload = {
        "umnetId": "SHARMAA2",
        "password": "akshay123",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert b'"success"' in response.data

def test_auth_user_password_incorrect(test_client, json_header, requests_mock):

    url = '/authUser'

    payload = {
        "umnetId": "SHARMAA2",
        "password": "akshay234567",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert b'"Incorrect umnetId or password"' in response.data

def test_auth_user_umnetid_incorrect(test_client, json_header, requests_mock):

    url = '/authUser'

    payload = {
        "umnetId": "SHARMAA3",
        "password": "akshay123",
    }

    response = test_client.post(
        url, data=json.dumps(payload), headers=json_header)
    assert b'"Incorrect umnetId or password"' in response.data
