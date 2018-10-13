from flask import Flask
from flask_restful import Api

import sqlite3


def get_conn():
    conn = sqlite3.connect('messages.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['DEBUG'] = True
api = Api(app)

from app import messages