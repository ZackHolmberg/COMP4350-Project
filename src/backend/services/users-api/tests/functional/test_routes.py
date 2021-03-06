import pytest
from unittest.mock import patch
from src.databases import database_init
import mongomock
import json

with patch.object(database_init, 'create_users_db', return_value=mongomock.MongoClient()):
    from src.app import app
    from src.app import mongo

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
def test_db_patch():
    mongo.db.create_collection("users")

    mongo.db.users.insert_one({"first_name" : "Akshay", "last_name" : "Sharma", "umnetID" : "SHARMAA2", "password" : "akshay123", "public_key" : "akshay_pk"})
    mongo.db.users.insert_one({"first_name" : "Abhi", "last_name" : "Sachdev", "umnetID" : "SACHDEV1", "password" : "abhi123", "public_key" : "abhi_pk"})
    mongo.db.users.create_index("umnetID", unique=True)
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


def test_insert_user(test_client, test_db_patch, json_header):
    url = '/create'
    
    payload = {
        "first_name" : "Madison",
        "last_name" : "Fines",
        "umnetID" : "FINESM1",
        "password" : "madison123",
        "public_key" : "madison_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)
    assert b'User Madison Fines added successfully! :)' in response.data

    user = mongo.db.users.find_one({"umnetID" : "FINESM1"})
    assert user is not None

    # remove the added user to maintain the state of the db
    mongo.db.users.delete_one({"umnetID" : "FINESM1"})


def test_get_all_users(test_client, test_db_patch):
    
    url = '/all'

    # print("USERS:")
    # for usr in mongo.db.users.find({}):
    #     print(usr)

    response = test_client.get(url)

    assert b'"umnetID":"SHARMAA2"' in response.data
    assert b'"umnetID":"SACHDEV1"' in response.data


def test_create_error_duplicate_umnetID_and_password(test_client, test_db_patch, json_header):
    
    url = '/create'
    
    # duplicate umnetID
    payload = {
        "first_name" : "Zack",
        "last_name" : "Holmberg",
        "umnetID" : "SHARMAA2",
        "password" : "zack123",
        "public_key" : "zack_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b"Database schema validation failed! Please check your input and try again." in response.data

    
    # duplicate private key 
    payload = {
        "first_name" : "Bob",
        "last_name" : "Dylan",
        "umnetID" : "DYLANB1",
        "password" : "bob123",
        "public_key" : "abhi_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b"Database schema validation failed! Please check your input and try again." in response.data


def test_create_error_incomplete_payload(test_client, test_db_patch, json_header):
    # TODO: send a request with missing payload params and assert for an incorrect payload failure
    url = '/create'
    
    # duplicate umnetID
    payload = {
        "first_name" : "Bob",
        "last_name" : "Dylan",
        "umnetID" : "SHARMAA2",
        "password" : "bob123"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b'Please send correct json payload' in response.data


def test_success_get_user_by_umnetID(test_client, test_db_patch):
    url = '/umnetID/SHARMAA2'

    response = test_client.get(url)

    assert b'"umnetID":"SHARMAA2"' in response.data

def test_failure_get_user_by_umnetID_user_not_found(test_client, test_db_patch):
    url = '/umnetID/DOESNTEXIST'

    response = test_client.get(url)

    assert b'"user not found!"' in response.data

def test_success_update_user(test_client, test_db_patch, json_header):
    url = '/update'

    payload = {
        "first_name" : "Akshay",
        "last_name" : "Sharma",
        "umnetID" : "SHARMAA2",
        "password" : "akshay234",
        "public_key" : "akshay_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    # Check the response to see if it's correct 
    assert b'User SHARMAA2 updated successfully! :)' in response.data

    # Check the db to see if the updates were successful
    db_user = mongo.db.users.find_one({"umnetID" : "SHARMAA2"})
    assert 'akshay234' == db_user["password"]

    # change the password back to original (bonus test lol)
    payload = {
        "first_name" : "Akshay",
        "last_name" : "Sharma",
        "umnetID" : "SHARMAA2",
        "password" : "akshay123",
        "public_key" : "akshay_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    # Check if the response is correct
    assert b'User SHARMAA2 updated successfully! :)' in response.data

    # Check if the database was updated successfully
    db_user = mongo.db.users.find_one({"umnetID" : "SHARMAA2"})
    assert 'akshay123' == db_user["password"]


def test_failure_update_user_user_not_found(test_client, test_db_patch, json_header):
    url = '/update'

    payload = {
        "first_name" : "Fake",
        "last_name" : "User",
        "umnetID" : "DOES_NOT_EXIST",
        "password" : "fake123",
        "public_key" : "fake_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b"Database schema validation failed! Please check your input and try again." in response.data


def test_failure_update_user_incomplete_payload(test_client, test_db_patch, json_header):
    url = '/update'

    # payload with missing public key
    payload = {
        "first_name" : "Akshay",
        "last_name" : "Sharma",
        "umnetID" : "SHARMAA2",
        "password" : "akshay123"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b'Please send correct json payload' in response.data
