import os

from flask import Flask

from .blockchain import *

app = Flask(__name__)

is_master = not os.environ.get("BACKUP", False)
peers = []

if is_master:
    peers.append("http://blockchain-backup:5000")

from src import routes

if is_master:
    routes.query_peers(peers)
else:
    routes.query_peers(["http://blockchain:5000"])