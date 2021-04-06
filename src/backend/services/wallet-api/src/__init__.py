"""init for the module containing the wallet api routes"""
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from src import routes
