from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

blockchain_wallet_url = "http://blockchain:5000/wallet/{:s}"

from src import routes
