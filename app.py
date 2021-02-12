import random
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Welcome</h1>"


@app.route('/api/say_hi', methods=['GET'])
def respond():
    response = {"greeting": random.choice(["Hello!", "Greetings!"])}
    return jsonify(response)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
