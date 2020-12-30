from flask import Flask
from citywok_ms.config import Config


def create_app(config_class=Config):
    # create the app instance
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    # TODO:
    
    with app.app_context():
        # imports
        # TODO:
        
        # blueprints
        # TODO:
        
        return app
    