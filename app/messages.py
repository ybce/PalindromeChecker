from flask import render_template, make_response, request
from flask import jsonify
from app import get_conn
from utils import checkPalindrome, get_messages

from app import app

@app.route('/')
def index():
    headers = {'Content-Type': 'text/html'}
    messages = get_messages()
    return make_response(render_template('index.html', title="Welcome to the Palindrome Checker", messages=messages),
                         200, headers)

@app.route('/check/', methods=['POST'])
def post():
    c = get_conn()
    message_id = request.json["message_id"]
    id = (message_id, )
    query = c.execute("SELECT message FROM messages WHERE message_id = ?", id)
    message = query.fetchone()["message"]
    palindrome = int(checkPalindrome(message))
    print palindrome
    m = (palindrome, message_id)
    c.execute("UPDATE messages SET palindrome=? WHERE message_id=?", m)
    c.commit()
    c.close()
    return_value = {
        "palindrome": palindrome,
        "message_id": message_id
    }
    return make_response(jsonify(return_value), 200)


@app.route('/delete/', methods=['DELETE'])
def delete():
    c = get_conn()
    message_id = request.json["message_id"]
    m = (message_id, )
    c.execute("DELETE FROM messages WHERE message_id=?", m)
    c.commit()
    c.close()
    return_value = {
        "status": "Your message has been deleted",
        "message_id": message_id
    }
    return make_response(jsonify(return_value), 200)

@app.route('/add/', methods=['POST'])
def add_word():
    c = get_conn()
    message = request.json["value"]
    m = (message, )
    query = c.execute("INSERT INTO messages (message) VALUES (?);", m)
    m_id = query.lastrowid
    c.commit()
    c.close()
    return_value = {
        "status": "Your message has been added",
        "message": message,
        "message_id": m_id
    }
    return make_response(jsonify(return_value), 201)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
