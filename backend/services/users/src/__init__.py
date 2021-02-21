import sys, os
from flask import Flask

sys.path.append(os.path.join('..', ''))

for root, dirs, files in os.walk("./shared", topdown=False):
   for name in files:
      print(os.path.join(root, name))
   for name in dirs:
      print(os.path.join(root, name))

for root, dirs, files in os.walk("./users", topdown=False):
   for name in files:
      print(os.path.join(root, name))
   for name in dirs:
      print(os.path.join(root, name))

from shared import config
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config.from_object(config.Config())

app.config["MONGO_URI"] = 'mongodb://' + app.config['MONGODB_USERNAME'] + ':' + app.config['MONGODB_PASSWORD'] + '@' + app.config['MONGODB_HOSTNAME'] + ':27017/' + app.config['MONGODB_DATABASE'] 


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

print(db.list_collection_names())

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
