class Config():
    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # babel
    LANGUAGES = ['en', 'pt-PT', 'zh']
    BABEL_DEFAULT_LOCALE = 'zh'
