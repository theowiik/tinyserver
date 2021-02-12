import random
from flask import Flask, jsonify, abort

app = Flask(__name__)

cats = [
    {
        'id': 1,
        'name': u'Sir Cat',
        'description': u'Some text'
    },
    {
        'id': 2,
        'title': u'Mr Cat',
        'description': u'Some more text'
    }
]


@app.route('/')
def index():
    return "<h1>Welcome</h1>"


@app.route('/api/say_hi', methods=['GET'])
def respond():
    response = {"greeting": random.choice(["Hello!", "Greetings!"])}
    return jsonify(response)


@app.route('/api/cats', methods=['GET'])
def get_cats():
    return jsonify({"cats": cats})


@app.route('/api/cats/<int:cat_id>', methods=['GET'])
def get_cat(cat_id):
    cat = None

    for c in cats:
        if c['id'] == cat_id:
            cat = c
            break

    if not cat:
        abort(404)

    return jsonify({'cat': cat})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
