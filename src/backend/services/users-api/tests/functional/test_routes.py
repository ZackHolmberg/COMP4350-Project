import pytest
from unittest.mock import patch
from src.databases import database_init
import mongomock

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
    mongo.db.create_collection("users", validator=userSchema)

    mongo.db.users.insert_one({"first_name" : "Akshay", "last_name" : "sharma", "username" : "SHARMAA2", "password" : "akshay123", "public_key" : "akshay_pk"})
    mongo.db.users.create_index("username", unique=True)
    mongo.db.users.create_index("public_key", unique=True)
    
    print("curr users: ") 
    # print(mongo.db.users.find({}), file=sys.stderr)
    
    

def test_home_page(test_client, test_db_patch):
    # test GET query on '/' route

    url = '/'

    print("curr users in index: ")
    for usr in mongo.db.users.find({}):
        print(usr, file=sys.stderr)

    response = test_client.get(url)

    assert response.status_code == 200
    resp_msg = "Hello Users of " + mongo.db.name
    assert resp_msg.encode('utf-8') in response.data

def test_get_user(test_client, test_db_patch):
    mongo.db.users.insert_one({"first_name" : "Abhishek", "last_name" : "Sachdev", "username" : "SACHDEV1", "password" : "abhi123", "public_key" : "abhi_pk"})

    print("curr users in get user: ")
    for usr in mongo.db.users.find({}):
        print(usr, file=sys.stderr)

def test_get_user2(test_client, test_db_patch):
    # mongo.db.users.insert_one({"first_name" : "Abhishek", "last_name" : "sachdev", "username" : "SACHDEV1", "password" : "abhi123", "public_key" : "abhi_pk"})
    mongo.db.users.delete_one({"first_name" : "Abhishek"})
    print("curr users in get user2: ")
    for usr in mongo.db.users.find({}):
        print(usr, file=sys.stderr)
