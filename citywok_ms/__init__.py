import flask_babel
from flask import Flask, current_app, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import i18n
from flask_wtf.csrf import CSRFProtect

from citywok_ms.config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
babel = Babel()


def create_app(config_class=Config):
    # create the app instance
    app = Flask(__name__)
    app.config.from_object(config_class)
    i18n.get_locale = flask_babel.get_locale

    # init extensions
    db.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)

    with app.app_context():
        # imports
        from citywok_ms.employee.routes import employee
        from citywok_ms.supplier.routes import supplier
        # blueprints
        app.register_blueprint(employee)
        app.register_blueprint(supplier)

        return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
