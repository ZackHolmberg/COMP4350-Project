import sys, os
from flask import Flask

sys.path.append(os.path.join('..', ''))

from shared import config
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config.from_object(config.Config(''))

mongo = PyMongo(app)
db = mongo.db

userSchema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "privateKey"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "username must be a string and is required."
            },
            "privateKey": {
                "bsonType": "string",
                "description": "user requires a private key."
            }
        }
    }
}


if("users" not in db.list_collection_names()):
    db.create_collection("users")

db.command({
        "collMod": "users",
        "validator": userSchema,
        "validationLevel": "strict",
        "validationAction": "error"
    }
)


from src import routes
