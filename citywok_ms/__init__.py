import flask_babel
from flask import Flask, current_app, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import i18n
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment

import os


csrf = CSRFProtect()
db = SQLAlchemy()
babel = Babel()
moment = Moment()


def create_app(test_config=None, instance_path=None):
    # create the app instance
    app = Flask(__name__, instance_relative_config=True)

    if instance_path:
        app.instance_path = instance_path
    else:  # test: no cover
        os.makedirs(app.instance_path, exist_ok=True)

    # default
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path,"database.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        LANGUAGES=['en'],
        FLASK_ENV='development',
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads')
    )

    if test_config is None:  # test: no cover
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    i18n.get_locale = flask_babel.get_locale

    # init extensions
    db.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)
    moment.init_app(app)

    with app.app_context():
        # imports
        from citywok_ms.employee.routes import employee
        from citywok_ms.supplier.routes import supplier
        from citywok_ms.file.routes import file
        # blueprints
        app.register_blueprint(employee)
        app.register_blueprint(supplier)
        app.register_blueprint(file)

        return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
