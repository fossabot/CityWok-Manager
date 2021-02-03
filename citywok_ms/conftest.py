import pytest

from citywok_ms import create_app, db
from citywok_ms.models import Employee, Supplier
from datetime import date


@pytest.fixture(scope='class')
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


@pytest.fixture(scope='function')
def test_employees():
    e1 = Employee(first_name='TEST_1',
                  last_name='INFO',
                  sex='F',
                  id_type='passport',
                  id_number='123',
                  id_validity=date(2100, 1, 1),
                  nationality='US',
                  total_salary='1000',
                  taxed_salary='635.00')
    db.session.add(e1)

    e2 = Employee(first_name='TEST_2',
                  last_name='INFO',
                  sex='M',
                  id_type='passport',
                  id_number='123',
                  id_validity=date(2100, 1, 1),
                  nationality='PT',
                  total_salary='1500',
                  taxed_salary='635.00')
    db.session.add(e2)

    e3 = Employee(first_name='TEST_3',
                  last_name='INFO',
                  sex='F',
                  id_type='passport',
                  id_number='123',
                  id_validity=date(2100, 1, 1),
                  nationality='BR',
                  total_salary='1000',
                  taxed_salary='635.00',
                  active=False)
    db.session.add(e3)

    db.session.commit()
    yield
    db.drop_all()
    db.create_all()


@pytest.fixture(scope="function")
def test_suppliers():
    s1 = Supplier(name="TEST_1",
                  principal="P_1")
    db.session.add(s1)
    s2 = Supplier(name="TEST_2",
                  principal="P_2")
    db.session.add(s2)
    db.session.commit()
    yield
    db.session.query(Supplier).delete()
    db.session.commit()
