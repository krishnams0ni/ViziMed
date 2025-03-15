import os
from flask import Flask
from models import db
from routes import register_routes
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        if not os.path.exists("users.db"):
            db.create_all()
            print("Database created!")
    register_routes(app)
    return app
