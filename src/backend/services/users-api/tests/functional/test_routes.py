import pytest
from unittest.mock import patch
from src.databases import database_init
import mongomock
import json

with patch.object(database_init, 'create_users_db', return_value=mongomock.MongoClient()):
    from src.app import app
    from src.app import mongo

from src.databases.UserSchema import userSchema
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

    mongo.db.users.insert_one({"first_name" : "Akshay", "last_name" : "Sharma", "username" : "SHARMAA2", "password" : "akshay123", "public_key" : "akshay_pk"})
    mongo.db.users.insert_one({"first_name" : "Abhi", "last_name" : "Sachdev", "username" : "SACHDEV1", "password" : "abhi123", "public_key" : "abhi_pk"})
    mongo.db.users.create_index("username", unique=True)
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
        "username" : "FINESM1",
        "password" : "madison123",
        "public_key" : "madison_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)
    assert b'User Madison Fines added successfully! :)' in response.data

    user = mongo.db.users.find_one({"username" : "FINESM1"})
    assert user is not None

    # remove the added user to maintain the state of the db
    mongo.db.users.delete_one({"username" : "FINESM1"})


def test_get_all_users(test_client, test_db_patch):
    
    url = '/all'

    response = test_client.get(url)

    assert b'"username":"SHARMAA2"' in response.data
    assert b'"username":"SACHDEV1"' in response.data


def test_create_error_duplicate_username_and_password(test_client, test_db_patch, json_header):
    
    url = '/create'
    
    # duplicate username
    payload = {
        "first_name" : "Bob",
        "last_name" : "Dylan",
        "username" : "SHARMAA2",
        "password" : "bob123",
        "public_key" : "bob_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b"Database schema validation failed! Please check your input and try again." in response.data

    
    # duplicate private key 
    payload = {
        "first_name" : "Bob",
        "last_name" : "Dylan",
        "username" : "DYLANB1",
        "password" : "bob123",
        "public_key" : "abhi_pk"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b"Database schema validation failed! Please check your input and try again." in response.data


def test_create_error_incomplete_payload(test_client, test_db_patch, json_header):
    # TODO: send a request with missing payload params and assert for an incorrect payload failure
    url = '/create'
    
    # duplicate username
    payload = {
        "first_name" : "Bob",
        "last_name" : "Dylan",
        "username" : "SHARMAA2",
        "password" : "bob123"
        }

    response = test_client.post(url, data=json.dumps(payload), headers=json_header)

    assert b'Please send correct json payload' in response.data
    print()


def test_update_user(test_client, test_db_patch):
    # TODO: update an attribure of one of the existing users and assert if the change was successful
    print()

def test_success_get_user_by_username(test_client, test_db_patch):
    # TODO: get user with the existing SHARMAA2 id and check for correct response
    url = '/username/SHARMAA2'

    response = test_client.get(url)

    assert b'"username":"SHARMAA2"' in response.data

def test_failure_get_user_by_username_user_not_found(test_client, test_db_patch):
    url = '/username/DOESNTEXIST'

    response = test_client.get(url)

    assert b'"user not found!"' in response.data
