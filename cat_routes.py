from flask import Blueprint, jsonify, abort, request

from app import db
from models import Cat, Human

cat_routes = Blueprint('cat_routes', __name__)


@cat_routes.route('/api/cats', methods=['GET'])
def get_cats():
    cats = Cat.query.all()
    return jsonify({"cats": [cat.to_dict() for cat in cats]})


@cat_routes.route('/api/cats/<int:cat_id>', methods=['GET'])
def get_cat(cat_id):
    cat = Cat.query.filter_by(id=cat_id).first()
    if not cat:
        abort(404)
    return jsonify({'cat': cat.to_dict()})


@cat_routes.route('/api/cats', methods=['POST'])
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


@cat_routes.route('/api/cats/<int:cat_id>/set_human/<string:human_name>', methods=['PATCH'])
def set_human(cat_id, human_name):
    cat = Cat.query.filter_by(id=cat_id).first()
    human = Human.query.filter_by(name=human_name).first()

    if not cat or not human:
        abort(404)

    cat.human = human
    db.session.commit()

    return jsonify({'cat': cat.to_dict()})
