from flask import Blueprint, jsonify, abort, request

from app import db
from models import Human

human_routes = Blueprint('human_routes', __name__)


@human_routes.route('/api/humans', methods=['GET'])
def get_humans():
    humans = Human.query.all()
    return jsonify({"humans": [human.to_dict() for human in humans]})


@human_routes.route('/api/humans', methods=['POST'])
def create_human():
    name = request.get_json()['name']

    if not name:
        abort(400)

    human = Human(name=name)
    db.session.add(human)
    db.session.commit()

    return jsonify({"human": human.to_dict()})


@human_routes.route('/api/humans/<string:human_name>', methods=['GET'])
def get_human(human_name):
    human = Human.query.filter_by(name=human_name).first()
    print(human)
    if not human:
        abort(404)
    return jsonify({'human': human.to_dict()})
