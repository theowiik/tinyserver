from sqlalchemy_serializer import SerializerMixin

from app import db


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
