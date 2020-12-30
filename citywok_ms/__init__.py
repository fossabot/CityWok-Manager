from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from citywok_ms.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    # create the app instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)

    with app.app_context():
        # imports
        # TODO:

        # blueprints
        # TODO:

        return app
