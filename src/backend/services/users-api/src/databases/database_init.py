from flask_pymongo import PyMongo

def create_users_db(app, schema):
    mongo = PyMongo(app)
    db = mongo.db

    # Create the users collection if it's not already there
    if("users" not in db.list_collection_names()):
        db.create_collection("users")

    # Make the username and public_key into unique indexes
    db.users.create_index("umnetId", unique=True)
    db.users.create_index("public_key", unique=True)

    # Add the validator
    db.command({
            "collMod": "users",
            "validator": schema,
            "validationLevel": "strict",
            "validationAction": "error"
        }
    )

    return mongo
