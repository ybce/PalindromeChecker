from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from flask import jsonify
import re

import sqlite3

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['DEBUG'] = True
api = Api(app)

def get_conn():
    conn = sqlite3.connect('messages.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_messages():
    c = get_conn()
    query = c.execute("select * from messages;")
    return_value = jsonify({'messages': [dict(row) for row in query.fetchall()]})
    return return_value.json["messages"]

class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        messages = get_messages()
        return make_response(render_template('index.html', title="Welcome to the Palindrome Checker", messages=messages), 200, headers)

class Check(Resource):
    def checkPalindrome(self, message):
        message = re.sub(r"\s+", "", message)
        return message == message[::-1]

    def post(self):
        c = get_conn()
        message_id = request.json["message_id"]
        id = (message_id, )
        query = c.execute("SELECT message FROM messages WHERE message_id = ?", id)
        message = query.fetchone()["message"]
        palindrome = int(self.checkPalindrome(message))
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

class Delete(Resource):
    def delete(self):
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

class Add(Resource):
    def post(self):
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
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500

@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403


api.add_resource(Index, '/')
api.add_resource(Check, '/check/')
api.add_resource(Delete, '/delete/')
api.add_resource(Add, '/add/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
