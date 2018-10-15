from flask import Flask
from flask_restful import Api
import json
import sqlite3


def get_conn():
    conn = sqlite3.connect('messages.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True


from app import messages