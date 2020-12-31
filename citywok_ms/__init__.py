from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from citywok_ms.config import Config

db = SQLAlchemy()
babel = Babel()


def create_app(config_class=Config):
    # create the app instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    babel.init_app(app)

    with app.app_context():
        # imports
        # TODO:

        # blueprints
        # TODO:

        return app


@babel.localeselector
def get_local():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
