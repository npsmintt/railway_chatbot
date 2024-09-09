from flask import Flask, render_template, request, jsonify, session
from models.chat import get_response

from models.ticket_rules import *
import os

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["myChatDatabase"]
book_db = db["booking"]

app = Flask(__name__, template_folder=os.path.join(
    os.path.dirname(__file__), 'templates'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    user_input = request.form["message"]
    response = get_response(user_input)
    return jsonify({"response": response})

@app.route("/clear_database", methods=["POST"])
def clear_database():
    book_db.delete_many({})
    return "Databases cleared."

clear_database()

if __name__ == '__main__':
    app.secret_key = 'Group 3 is the best'
    app.run(host='0.0.0.0', port=5100, debug=True)
    