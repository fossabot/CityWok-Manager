import pytest

from citywok_ms import create_app, db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()
            yield testing_client  # this is where the testing happens!
            db.drop_all()
