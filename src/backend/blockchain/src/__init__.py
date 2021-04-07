"""init file for the blockchain api"""
from flask import Flask
from .blockchain import *

app = Flask(__name__)

from src import routes
