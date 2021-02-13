from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# Routes
from cat_routes import cat_routes
from human_routes import human_routes

app.register_blueprint(cat_routes)
app.register_blueprint(human_routes)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
