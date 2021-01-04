from citywok_ms import db
from citywok_ms.models import Employee


def test_get(test_client):
    response = test_client.get('/employee/new')
    assert response.status_code == 200


def test_full_info(test_client):
    data = dict(first_name='FULL',
                last_name='INFO',
                zh_name='中文',
                sex='M',
                birthday='2020-01-01',
                contact='123123123',
                email='123@mail.com',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                nif='123123',
                niss='321321',
                employment_date='2021-01-01',
                total_salary='1000',
                taxed_salary='635.00',
                remark='REMARK')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Successfully' in response.data.decode('utf-8')
    assert 'This field is required' not in response.data.decode('utf-8')

    assert len(db.session.query(Employee).filter_by(
        first_name="FULL").all()) == 1


def test_basic_info(test_client):
    data = dict(first_name='BASIC',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)

    assert response.status_code == 200
    assert 'Successfully' in response.data.decode('utf-8')
    assert 'This field is required' not in response.data.decode('utf-8')

    assert len(db.session.query(Employee).all()) == 2

    assert len(db.session.query(Employee).filter_by(
        first_name="BASIC").all()) == 1


def test_empty(test_client):
    response = test_client.post('/employee/new',
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_first_name(test_client):
    data = dict(first_name='',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_last_name(test_client):
    data = dict(first_name='TEST',
                last_name='',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_sex(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='X',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Not a valid choice' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2

    data['sex'] = ''
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_id_type(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='F',
                id_type='xxx',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Not a valid choice' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2

    data['id_type'] = ''
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_id_number(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_id_validity(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='1999-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'ID has expired' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_nationality(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='XXX',
                total_salary='1000',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid Choice' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2

    data['nationality'] = ''
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_total_salary(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='',
                taxed_salary='635.00')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2

    data['total_salary'] = 'abc'
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'Not a valid decimal value' in response.data.decode(
        'utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_invalide_taxed_salary(test_client):
    data = dict(first_name='TEST',
                last_name='INFO',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This field is required' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_duplicate_nif(test_client):
    data = dict(first_name='TEST',
                last_name='TEST',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00',
                nif='123123')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This NIF already existe' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2


def test_duplicate_niss(test_client):
    data = dict(first_name='TEST',
                last_name='TEST',
                sex='F',
                id_type='passport',
                id_number='123',
                id_validity='2100-01-01',
                nationality='US',
                total_salary='1000',
                taxed_salary='635.00',
                niss='321321')
    response = test_client.post('/employee/new',
                                data=data,
                                follow_redirects=True)
    assert response.status_code == 200
    assert 'This NISS already existe' in response.data.decode('utf-8')
    assert 'Successfully' not in response.data.decode('utf-8')
    assert len(db.session.query(Employee).all()) == 2
