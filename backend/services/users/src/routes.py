from src import app
from flask import request, jsonify
from src import db


@app.route("/")
def index():
    return jsonify(
        status=True,
        message="Hello Users of " + db.name
    )


@app.route("/users")
def users():
    print(db.values)
    userList = db.users.find()
    
    user = {}
    data = []

    for usr in userList:
        user = {
            'name' : usr['name'],
            'privateKey' : usr['privateKey']
        }
        data.append(user)

    return jsonify(
        status=True,
        data=data
    )

@app.route('/users', methods=['POST'])
def createUser():
    data = request.get_json(force=True)
    user = {
        'name' : data['name'],
        'privateKey' : data['privateKey']
    }
    db.users.insert_one(user)

    return jsonify(
        status = True,
        message= 'User added successfully! :)'
    ), 201