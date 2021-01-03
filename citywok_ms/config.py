import os


class Config():
    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # babel
    LANGUAGES = ['en', 'pt-PT', 'zh']
    BABEL_DEFAULT_LOCALE = 'zh'

    # CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY')
