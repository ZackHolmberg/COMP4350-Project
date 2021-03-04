from src.app import app
from flask import request, jsonify
from src.app import mongo
import sys, os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString, config


@app.route("/")
def index():
    return jsonify(
        status=True,
        message="Hello Users of " + mongo.db.name
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    try:
        username = data['username']
        password = data['password']
    except Exception as e:
        return jsonify(err= FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    user = mongo.db.users.find_one({"username":username})

    return jsonify(success = (user["password"] == password))

@app.route("/getUserInfo", methods=["POST"])
def getUserInfo():
    data = request.get_json(force=True)

    try:
        username = data['username']
    
    except Exception as e:
          return jsonify(err=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    user = mongo.db.users.find_one({'username' : username})

    try:
        data = {
            'first_name' : user['first_name'],
            'last_name' : user['last_name'],
            'username' : user['username'],
            'public_key' : user['public_key']
        }
    except Exception as e:
        data = "user not found!"

    return jsonify(
        status=True,
        data = data
    )

@app.route("/users")
def users():
    userList = mongo.db.users.find()
    
    user = {}
    data = []

    for usr in userList:
        user = {
            'first_name' : usr['first_name'],
            'last_name' : usr['last_name'],
            'username' : usr['username'],
            'public_key' : usr['public_key']
        }
        data.append(user)

    return jsonify(
        status=True,
        data=data
    )

@app.route('/users', methods=['POST'])
def createUser():
    data = request.get_json(force=True)
    try: 
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        username = data["username"]
        public_key = data["public_key"]
    
    except Exception as e:
        return jsonify(err=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value
    
    user = {
        "first_name" : first_name,
        "last_name" : last_name,
        "username" : username,
        "password" : password,
        "public_key" : public_key
    }

    try:
        mongo.db.users.insert_one(user)
    except Exception as e:
        #TODO: add this error code to the failure return strings
        return jsonify(err="database schema validation failed! please check your input and try again."), HttpCode.BAD_REQUEST.value

    return jsonify(
        status = True,
        message= 'User ' + first_name + ' ' + last_name + ' added successfully! :)'
    ), 201