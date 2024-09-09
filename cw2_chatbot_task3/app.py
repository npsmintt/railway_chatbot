from flask import Flask, render_template, request, jsonify, session
from models.chat import get_response
import os

app = Flask(__name__, template_folder=os.path.join(
    os.path.dirname(__file__), 'templates'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    user_input = request.form["message"]
    response = get_response(user_input)
    return jsonify(({"response": response}))

if __name__ == '__main__':
    app.secret_key = 'Group 3 is the best'
    app.run(debug=True, port=3000)