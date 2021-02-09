import pytest
import io
from tempfile import TemporaryDirectory
from citywok_ms import create_app, db
from citywok_ms.models import Employee, File, Supplier
from datetime import date, datetime


@pytest.fixture(scope='class')
def test_client():
    with TemporaryDirectory() as temp_dir:

        flask_app = create_app(test_config={
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'BABEL_DEFAULT_LOCALE': 'en',
            'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:"
        }, instance_path=temp_dir)

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


@pytest.fixture(scope="function")
def test_files(test_client, test_employees, test_suppliers):
    data = dict(
        file=(io.BytesIO(b'test_file_content'), "emp_1.pdf"),
    )
    test_client.post('/employee/1/upload',
                     data=data,
                     follow_redirects=True,
                     content_type='multipart/form-data')
    data = dict(
        file=(io.BytesIO(b'test_file_content'), "sup_1.png"),
    )
    test_client.post('/supplier/1/upload',
                     data=data,
                     follow_redirects=True,
                     content_type='multipart/form-data')
    db.session.query(File).get(2).delete_date = datetime.utcnow()
    db.session.commit()
    yield
    db.drop_all()
    db.create_all()
