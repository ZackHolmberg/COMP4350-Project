"""User-api module: contains the routes that users access to interact with the database"""
from flask import request, jsonify
from shared.exceptions import IncorrectCredentialsException, IncorrectPayloadException,\
     UserNotFoundException, DatabaseVerificationException
from shared.utils import BisonCoinUrls, send_post_request
from shared.httpcodes import HttpCode
from werkzeug.security import generate_password_hash, check_password_hash
from src.app import app, mongo


def get_user_from_db(umnetId, password):
    """
    Retrieves the user with the supplied umnetID from the database if the password is correct

            Parameters:
                    umnetId (string): A string umnetId that is to be retrieved
                    password (string): The password associated to the supplied umnetId

            Returns:
                    User (string): The user associated to the umnetId
                    error (string): if the password does not match the umnetId supplied
    """
    user = mongo.db.users.find_one({"umnetId": umnetId})
    if not user or not check_password_hash(user["password"], password):
        raise IncorrectCredentialsException()
    return user


@app.route("/")
def index():
    """
    endpoint to test if the service is running, returns a welcome string and status=True

            Parameters:
                    None

            Returns:
                    greeting message if the service is up
    """
    return jsonify(
        success=True,
        message="Hello Users of " + mongo.db.name
    )


@app.route("/login", methods=["POST"])
def login():
    """
    Login endpoint for users
            Parameters: through request:
                    umnetId (string): A string umnetId that is to be retrieved
                    password (string): The password associated to the supplied umnetId

            Returns:
                    User (string): returns user's name and public key on successful login
                    error (string)
    """
    data = request.get_json()
    try:
        umnetId = data['umnetId'].upper()
        password = data['password']
    except KeyError as error:
        raise IncorrectPayloadException() from error

    user = get_user_from_db(umnetId, password)
    data = {
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'public_key': user['public_key']
    }

    return jsonify(user=data)


@app.route("/umnetId/<umnetId>", methods=['GET'])
def get_user(umnetId):
    """
    Retrieves the information of the user associated with the supplied umnetId

            Parameters: through request:
                    umnetId (string): A string umnetId that is to be retrieved

            Returns:
                    data (string): User's information including public key, name, and umnetId
                    error (string): error with the approptiate message
    """
    user = mongo.db.users.find_one({'umnetId': umnetId.upper()})

    try:
        data = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'umnetId': user['umnetId'],
            'public_key': user['public_key']
        }
    except Exception as error:
        raise UserNotFoundException() from error

    return jsonify(
        success=True,
        data=data
    )


@app.route("/list", methods=['GET'])
def get_all_users():
    """
    Retrieves a list of all the users present in the database along with their information.

            Parameters: through request:
                    None

            Returns:
                    data (list of strings): list of users and their information
                    error (string): error with the approptiate message
    """
    user_list = mongo.db.users.find()

    user = {}
    data = []

    for usr in user_list:
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
    """
    Authentication endpoint for services

            Parameters: through request:
                    umnetId (string): A string umnetId that is to be retrieved
                    password (string): The password associated to the supplied umnetId

            Returns:
                    success (boolean): True if user is authenticated, else false
                    error (string): error with the approptiate message
    """
    data = request.get_json()
    try:
        umnetId = data["umnetId"].upper()
        password = data["password"]
    except KeyError as error:
        raise IncorrectPayloadException() from error

    # raises an error when user not found
    user = get_user_from_db(umnetId, password)
    assert "umnetId" in user
    return jsonify(success=True), HttpCode.OK.value


@app.route('/create', methods=['POST'])
def create_user():
    """
    Endpoint to create a new user

            Parameters: through request:
                    umnetId (string): User's umnetId
                    password (string): The password associated to the supplied umnetId
                    first_name (string): user's first name
                    last_name (string): user's last name
                    public key (string): user's public key

            Returns:
                    success (boolean): True if user is authenticated, else false
                    error (string): error with the approptiate message
    """
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        umnetId = data["umnetId"].upper()
        public_key = data["public_key"]

    except KeyError as error:
        raise IncorrectPayloadException() from error

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
        if "success" not in response.json():
            raise Exception(response.json())

    except Exception as error:
        raise DatabaseVerificationException(str(error)) from error

    return jsonify(
        success=True,
    ), HttpCode.CREATED.value


@app.route('/update', methods=['POST'])
def update_user():
    """
    Endpoint to update a user's information

            Parameters: through request:
                    umnetId (string): User's umnetId
                    password (string): The password associated to the supplied umnetId
                    first_name (string): user's first name
                    last_name (string): user's last name
                    public key (string): user's public key

            Returns:
                    success (boolean): True if user is authenticated, else false
                    error (string): error with the approptiate message
    """
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        curr_password = data["curr_password"]
        new_password = data["new_password"]
        umnetId = data["umnetId"].upper()
    except KeyError as error:
        raise IncorrectPayloadException() from error

    user = get_user_from_db(umnetId, curr_password)

    new_password_hash = generate_password_hash(new_password, method='sha256')
    updated_user = {
        "first_name": first_name,
        "last_name": last_name,
        "password": new_password_hash,
        "public_key": user["public_key"]
    }

    try:
        mongo.db.users.update_one(
            {"umnetId": umnetId}, {"$set": updated_user})

    except Exception as error:
        raise DatabaseVerificationException(str(error)) from error

    return jsonify(
        success=True
    ), HttpCode.OK.value


@app.errorhandler(DatabaseVerificationException)
def handle_database_error(error):
    """
    method to handle database verification exception

            Parameters:
                    error: The error that occured in the endpoint

            Returns:
                    error message with faillure return code
    """
    return jsonify(database_error=error.error_message, error=error.json_message), error.return_code


@app.errorhandler(UserNotFoundException)
@app.errorhandler(IncorrectCredentialsException)
@app.errorhandler(IncorrectPayloadException)
def handle_userapi_error(error):
    """
    method to handle user not found, incorrect credentials and incorrect payload

            Parameters:
                    error: The error that occured in the endpoint

            Returns:
                    error message as json and return code
    """
    return jsonify(error=error.json_message), error.return_code
