from flask import Flask
from .blockchain import *

app = Flask(__name__)

from src import routes
