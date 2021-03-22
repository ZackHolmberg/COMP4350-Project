from src.app import app, mongo, HttpCode
from flask import request, jsonify
from shared.exceptions import IncorrectCredentialsException, IncorrectPayloadException, UserNotFoundException, DatabaseVerificationException
from shared.utils import BisonCoinUrls, send_post_request

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
        umnetId = data['umnetId'].upper()
        password = data['password']
    except KeyError as e:
        raise IncorrectPayloadException()

    try:
        user = mongo.db.users.find_one({"umnetId": umnetId})
        correct_credentials = user["password"] == password
    except Exception as e:
        raise UserNotFoundException()

    if not correct_credentials:
        raise IncorrectCredentialsException()

    data = {
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'public_key': user['public_key']
    }

    return jsonify(user=data)


@app.route("/umnetId/<umnetId>", methods=['GET'])
def get_user(umnetId):
    user = mongo.db.users.find_one({'umnetId': umnetId.upper()})

    try:
        data = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'umnetId': user['umnetId'],
            'public_key': user['public_key']
        }
    except Exception as e:
        raise UserNotFoundException()

    return jsonify(
        success=True,
        data=data
    )


@app.route("/list", methods=['GET'])
def get_all_users():
    userList = mongo.db.users.find()

    user = {}
    data = []

    for usr in userList:
        user = {
            'first_name': usr['first_name'],
            'last_name': usr['last_name'],
            'umnetId': usr['umnetId'],
            'public_key': usr['public_key']
        }
        data.append(user)

    return jsonify(
        success=True,
        data=data
    )


@app.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        umnetId = data["umnetId"].upper()
        public_key = data["public_key"]

    except KeyError as e:
        raise IncorrectPayloadException()

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "umnetId": umnetId,
        "password": password,
        "public_key": public_key
    }

    try:
        response = send_post_request( BisonCoinUrls.blockchain_wallet_url.format("addWallet"), {"umnetId": umnetId.strip()})
        if not "success" in response.json():
            raise Exception(response.json())

        mongo.db.users.insert_one(user)

    except Exception as e:
        raise DatabaseVerificationException(str(e))

    return jsonify(
        success=True,
    ), HttpCode.CREATED.value


@app.route('/update', methods=['POST'])
def update_user():
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        curr_password = data["curr_password"]
        new_password = data["new_password"]
        umnetId = data["umnetId"].upper()
    except KeyError as e:
        raise IncorrectPayloadException()

    usr = mongo.db.users.find_one({"umnetId": umnetId})

    if usr is None:
        raise DatabaseVerificationException("user doesn't exist")

    if usr["password"] != curr_password:
        raise DatabaseVerificationException("password verification failed")

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "password": new_password,
        "public_key": usr["public_key"]
    }

    try:
        res = mongo.db.users.update_one({"umnetId": umnetId}, {"$set": user})

    except Exception as e:
        raise DatabaseVerificationException(str(e))

    return jsonify(
        success=True
    ), HttpCode.OK.value


@app.errorhandler(DatabaseVerificationException)
def handle_database_error(e):
    return jsonify(database_error=e.error_message, error=e.json_message), e.return_code


@app.errorhandler(UserNotFoundException)
@app.errorhandler(IncorrectPayloadException)
def handle_userapi_error(e):
    return jsonify(error=e.json_message), e.return_code
