from app import get_conn
import re
from flask import jsonify

def get_messages():
    c = get_conn()
    query = c.execute("select * from messages;")
    return_value = jsonify({'messages': [dict(row) for row in query.fetchall()]})
    c.close()
    return return_value.json["messages"]

def checkPalindrome(message):
    message = re.sub(r"\s+", "", message)
    return message == message[::-1]