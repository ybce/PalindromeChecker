from flask import render_template, make_response, request
from flask import jsonify
from app import get_conn
from utils import checkPalindrome, get_messages, checkMessage

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
    if checkMessage(message):
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
    else:
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("400.html", code=400), 400, headers)


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html', code=400), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', code=404), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', code=500), 500

@app.errorhandler(403)
def unauthorized(e):
    return render_template('403.html', code=403), 403