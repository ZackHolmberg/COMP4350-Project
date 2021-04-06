from flask import Flask
from .blockchain import *
import os
app = Flask(__name__)

is_master = not os.environ.get('BACKUP', False)
peers = []

if is_master:
    peers.append("http://blockchain-backup:5000")

from src import routes

if is_master:
    routes.query_peer(peers)