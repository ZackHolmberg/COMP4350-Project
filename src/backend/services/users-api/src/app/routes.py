from src.app import app, mongo, HttpCode
from flask import request, jsonify
from shared.exceptions import IncorrectCredentialsException, IncorrectPayloadException, UserNotFoundException, DatabaseVerificationException
from shared.utils import BisonCoinUrls, send_post_request
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_from_db(umnetId, password):
    user = mongo.db.users.find_one({"umnetId": umnetId})
    if not user or not check_password_hash(user["password"], password):
        raise IncorrectCredentialsException()
    return user


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

    user = get_user_from_db(umnetId, password)
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


@app.route('/authUser', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    try:
        umnetId = data["umnetId"].upper()
        password = data["password"]
    except KeyError as e:
        raise IncorrectPayloadException()

    # raises an error when user not found
    user = get_user_from_db(umnetId, password)
    assert "umnetId" in user
    return jsonify(success=True), HttpCode.OK.value


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
        "password": generate_password_hash(password, method='sha256'),
        "public_key": public_key
    }

    try:
        mongo.db.users.insert_one(user)
        response = send_post_request(BisonCoinUrls.blockchain_wallet_url.format(
            "addWallet"), {"umnetId": umnetId.strip()})
        if not "success" in response.json():
            raise Exception(response.json())

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

    user = get_user_from_db(umnetId, curr_password)

    new_password_hash = generate_password_hash(new_password, method='sha256')
    updated_user = {
        "first_name": first_name,
        "last_name": last_name,
        "password": new_password_hash,
        "public_key": user["public_key"]
    }

    try:
        res = mongo.db.users.update_one(
            {"umnetId": umnetId}, {"$set": updated_user})

    except Exception as e:
        raise DatabaseVerificationException(str(e))

    return jsonify(
        success=True
    ), HttpCode.OK.value


@app.errorhandler(DatabaseVerificationException)
def handle_database_error(e):
    return jsonify(database_error=e.error_message, error=e.json_message), e.return_code


@app.errorhandler(UserNotFoundException)
@app.errorhandler(IncorrectCredentialsException)
@app.errorhandler(IncorrectPayloadException)
def handle_userapi_error(e):
    return jsonify(error=e.json_message), e.return_code
