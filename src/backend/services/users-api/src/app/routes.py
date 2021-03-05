from src.app import app
from flask import request, jsonify
from src.app import mongo
import sys, os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString, config

# TODO: add an endpoint to update a user

@app.route("/")
def index():
    return jsonify(
        status=True,
        message="Hello Users of " + mongo.db.name
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    try:
        username = data['username']
        password = data['password']
    except Exception as e:
        return jsonify(err= FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    user = mongo.db.users.find_one({"username":username})

    return jsonify(success = (user["password"] == password))

@app.route("/username/<username>")
def getUserInfo(username):

    user = mongo.db.users.find_one({'username' : username.upper()})

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

@app.route("/all")
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

@app.route('/create', methods=['POST'])
def createUser():
    data = request.get_json()
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
        "username" : username.upper(),
        "password" : password,
        "public_key" : public_key
    }

    try:
        mongo.db.users.insert_one(user)
    except Exception as e:
        return jsonify(err=FailureReturnString.DATABASE_VERIFICATION_FAILURE.value, error=str(e)), HttpCode.BAD_REQUEST.value

    return jsonify(
        status = True,
        message= 'User ' + first_name + ' ' + last_name + ' added successfully! :)'
    ), 201

@app.route('/update', methods=['POST'])
def updateUser():
    data = request.get_json()
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
        "password" : password,
        "public_key" : public_key
    }

    try:
        if mongo.db.users.find_one({"username" : username.upper()}) is None:
            raise Exception("user doesn't exist")
        
        res = mongo.db.users.update_one({"username" : username.upper()}, {"$set" : user})
    except Exception as e:
        return jsonify(err=FailureReturnString.DATABASE_VERIFICATION_FAILURE.value, error=str(e)), HttpCode.BAD_REQUEST.value

    return jsonify(
        status = True,
        message= 'User ' + username +' updated successfully! :)'
    ), 201

