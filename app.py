import random
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# Init
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


# ORM
class Cat(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    coolness = db.Column(db.Float)


# Routes
@app.route('/')
def index():
    return (
        "<h1>Welcome to my cool site</h1>\n"
        "<img src='https://images.unsplash.com/photo-1555685812-4b943f1cb0eb?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'/>"
    )


@app.route('/api/say_hi', methods=['GET'])
def respond():
    response = {"greeting": random.choice(["Hello!", "Greetings!"])}
    return jsonify(response)


@app.route('/api/cats', methods=['GET'])
def get_cats():
    cats = Cat.query.all()
    return jsonify({"cats": [cat.to_dict() for cat in cats]})


@app.route('/api/cats/<int:cat_id>', methods=['GET'])
def get_cat(cat_id):
    cat = Cat.query.filter_by(id=cat_id).first()
    if not cat:
        abort(404)
    return jsonify({'cat': cat.to_dict()})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
