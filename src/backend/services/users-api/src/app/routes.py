from src.app import app
from flask import request, jsonify
from src.app import mongo
import sys
import os

if os.environ.get('SERVICE_IN_DOCKER', False):
    sys.path.append(os.path.abspath(os.path.join('..', '')))
else:
    sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared import HttpCode, FailureReturnString


@app.route("/")
def index():
    return jsonify(
        success=True,
        message="Hello Users of " + mongo.db.name
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    try:
        umnetID = data['umnetID'].upper()
        password = data['password']
    except Exception as e:
        return jsonify(error=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    user = mongo.db.users.find_one({"umnetID": umnetID})

    return jsonify(success=(user["password"] == password))


@app.route("/umnetID/<umnetID>", methods=['GET'])
def getUser(umnetID):

    user = mongo.db.users.find_one({'umnetID': umnetID.upper()})

    try:
        data = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'umnetID': user['umnetID'],
            'public_key': user['public_key']
        }
    except Exception as e:
        data = "user not found!"

    return jsonify(
        success=True,
        data=data
    )


@app.route("/list", methods=['GET'])
def getUsers():
    userList = mongo.db.users.find()

    user = {}
    data = []

    for usr in userList:
        user = {
            'first_name': usr['first_name'],
            'last_name': usr['last_name'],
            'umnetID': usr['umnetID'],
            'public_key': usr['public_key']
        }
        data.append(user)

    return jsonify(
        success=True,
        data=data
    )


@app.route('/create', methods=['POST'])
def createUser():
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        umnetID = data["umnetID"]
        public_key = data["public_key"]

    except Exception as e:
        return jsonify(error=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "umnetID": umnetID.upper(),
        "password": password,
        "public_key": public_key
    }

    try:
        mongo.db.users.insert_one(user)
    except Exception as e:
        return jsonify(error=FailureReturnString.DATABASE_VERIFICATION_FAILURE.value, err=str(e)), HttpCode.BAD_REQUEST.value

    return jsonify(
        success=True,
    ), 201


@app.route('/update', methods=['POST'])
def updateUser():
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        curr_password = data["curr_password"]
        new_password = data["new_password"]
        umnetID = data["umnetID"]
        public_key = data["public_key"]

    except Exception as e:
        return jsonify(error=FailureReturnString.INCORRECT_PAYLOAD.value), HttpCode.BAD_REQUEST.value

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "password": new_password,
        "public_key": public_key
    }

    try:
        usr = mongo.db.users.find_one({"umnetID": umnetID.upper()})
        if usr is None:
            raise Exception("user doesn't exist")

        if usr["password"] != curr_password:
            raise Exception("password verification failed")

        res = mongo.db.users.update_one(
            {"umnetID": umnetID.upper()}, {"$set": user})
    except Exception as e:
        return jsonify(error=FailureReturnString.DATABASE_VERIFICATION_FAILURE.value, err=str(e)), HttpCode.BAD_REQUEST.value

    return jsonify(
        success=True,
    ), 200
