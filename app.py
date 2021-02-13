import random

from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# -------------------------------- INIT

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


# -------------------------------- ORM

class Human(db.Model, SerializerMixin):
    __tablename__ = 'humans'
    serialize_rules = ('-cats.human',)

    name = db.Column(db.String(30), primary_key=True)
    cats = db.relationship('Cat', back_populates='human')


class Cat(db.Model, SerializerMixin):
    __tablename__ = 'cats'
    serialize_rules = ('-human',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    coolness = db.Column(db.Float)
    human_name = db.Column(db.String, db.ForeignKey('humans.name'))
    human = db.relationship("Human", back_populates="cats")


# -------------------------------- ROUTES

# ------- RANDOM

@app.route('/api/say_hi', methods=['GET'])
def respond():
    response = {"greeting": random.choice(["Hello!", "Greetings!"])}
    return jsonify(response)


# ------- HUMANS

@app.route('/api/humans', methods=['GET'])
def get_humans():
    humans = Human.query.all()
    return jsonify({"humans": [human.to_dict() for human in humans]})


@app.route('/api/humans', methods=['POST'])
def create_human():
    name = request.get_json()['name']

    if not name:
        abort(400)

    human = Human(name=name)
    db.session.add(human)
    db.session.commit()

    return jsonify({"human": human.to_dict()})


@app.route('/api/humans/<string:human_name>', methods=['GET'])
def get_human(human_name):
    human = Human.query.filter_by(name=human_name).first()
    print(human)
    if not human:
        abort(404)
    return jsonify({'human': human.to_dict()})


# ------- CATS

@app.route('/api/cats', methods=['POST'])
def create_cat():
    json = request.get_json()
    name = json['name']
    coolness = json['coolness']

    if not name or not coolness:
        abort(400)

    cat = Cat(name=name, coolness=coolness)
    db.session.add(cat)
    db.session.commit()

    return jsonify({"cat": cat.to_dict()})


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


@app.route('/api/cats/<int:cat_id>/set_human/<string:human_name>', methods=['PATCH'])
def set_human(cat_id, human_name):
    cat = Cat.query.filter_by(id=cat_id).first()
    human = Human.query.filter_by(name=human_name).first()

    if not cat or not human:
        abort(404)

    cat.human = human
    db.session.commit()

    return jsonify({'cat': cat.to_dict()})


# -------------------------------- START

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
