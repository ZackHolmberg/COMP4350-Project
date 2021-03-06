import os
import sys

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from src.databases.database_init import create_users_db
from src.databases.UserSchema import userSchema

if os.environ.get("SERVICE_IN_DOCKER", False):
    sys.path.append(os.path.abspath(os.path.join("..", "")))
else:
    sys.path.append(os.path.abspath(os.path.join("../..", "")))

from shared import HttpCode, config

app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config.from_object(config.Config(""))

mongo = create_users_db(app, userSchema)


from src.app import routes
