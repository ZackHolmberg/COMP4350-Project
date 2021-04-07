"""init file for the mining-api"""
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app,cors_allowed_origins='*')

from src import routes
routes.transactions.start_thread()
