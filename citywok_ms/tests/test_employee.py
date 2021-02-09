import io
import os

from citywok_ms import db
from citywok_ms.models import Employee, File
from flask import request, current_app


class TestNew:
    def test_get(self, test_client):
        response = test_client.get('/employee/new')
        assert response.status_code == 200
        assert b"New Employee" in response.data

    def test_full_info(self, test_client):
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
        assert request.url.endswith('/employee/')
        assert 'Successfully' in response.data.decode('utf-8')
        assert 'This field is required' not in response.data.decode('utf-8')

        assert len(db.session.query(Employee).filter_by(
            first_name="FULL").all()) == 1

    def test_basic_info(self, test_client):
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
        assert request.url.endswith('/employee/')
        assert 'Successfully' in response.data.decode('utf-8')
        assert 'This field is required' not in response.data.decode('utf-8')

        assert len(db.session.query(Employee).all()) == 2

        assert len(db.session.query(Employee).filter_by(
            first_name="BASIC").all()) == 1

    def test_empty(self, test_client):
        response = test_client.post('/employee/new',
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'This field is required' in response.data.decode('utf-8')
        assert 'Successfully' not in response.data.decode('utf-8')
        assert len(db.session.query(Employee).all()) == 2

    def test_invalide_first_name(self, test_client):
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

    def test_invalide_last_name(self, test_client):
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

    def test_invalide_sex(self, test_client):
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

    def test_invalide_id_type(self, test_client):
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

    def test_invalide_id_number(self, test_client):
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

    def test_invalide_id_validity(self, test_client):
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

    def test_invalide_nationality(self, test_client):
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

    def test_invalide_total_salary(self, test_client):
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

    def test_invalide_taxed_salary(self, test_client):
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

    def test_duplicate_nif(self, test_client):
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

    def test_duplicate_niss(self, test_client):
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


class TestIndex:
    def test_get(self, test_client):
        response = test_client.get('/employee/')
        assert response.status_code == 200
        assert b'Employees' in response.data
        assert b'Active Employees' in response.data
        assert b'Inactive Employees' not in response.data

    def test_new_btn(self, test_client):
        response = test_client.get('/employee/')
        assert response.status_code == 200
        assert b'/employee/new' in response.data
        assert b'New' in response.data

    def test_detail_btn(self, test_client, test_employees):
        response = test_client.get('/employee/')
        assert response.status_code == 200
        assert b'/employee/1' in response.data
        assert b'/employee/2' in response.data
        assert b'/employee/4' not in response.data

    def test_employee_data(self, test_client, test_employees):
        response = test_client.get('/employee/')
        assert b'TEST_1' in response.data
        assert b'TEST_2' in response.data
        assert b'TEST_3' in response.data


class TestDetail:
    def test_get_valide(self, test_client, test_employees):
        response = test_client.get('/employee/1')
        assert response.status_code == 200
        assert b'TEST_1 INFO' in response.data
        assert b'Employee Detail' in response.data
        assert b'Files' in response.data
        assert b'New' in response.data

        response = test_client.get('/employee/2')
        assert response.status_code == 200
        assert b'TEST_2 INFO' in response.data
        assert b'Employee Detail' in response.data
        assert b'Files' in response.data
        assert b'New' in response.data

    def test_get_invalide(self, test_client, test_employees):
        response = test_client.get('/employee/101')
        assert response.status_code == 404

    def test_activate_btns(self, test_client, test_employees):
        response = test_client.get('/employee/1')
        assert response.status_code == 200
        assert b'employee/1/update' in response.data
        assert b'employee/1/inactivate' in response.data
        assert b'employee/1/activate' not in response.data
        assert b'Inactive' not in response.data

        assert b'New File' in response.data
        assert b'Show deleted files' in response.data
        assert b'Deleted Files' in response.data

    def test_inactivate_btns(self, test_client, test_employees):
        response = test_client.get('/employee/3')
        assert response.status_code == 200

        assert b'employee/3/update' in response.data
        assert b'employee/3/activate' in response.data
        assert b'employee/3/inactivate' not in response.data
        assert b'Inactive' in response.data


class TestOperation:
    def test_get_update(self, test_client, test_employees):
        response = test_client.get('/employee/1/update')
        assert response.status_code == 200
        assert b'Update employee' in response.data
        assert b'Update' in response.data
        assert b'TEST_1' in response.data
        assert b'INFO' in response.data

    def test_post_update(self, test_client, test_employees):
        data = dict(first_name='BASIC_UPDATED',
                    last_name='INFO',
                    sex='F',
                    id_type='passport',
                    id_number='123',
                    id_validity='2100-01-01',
                    nationality='US',
                    total_salary='1000',
                    taxed_salary='635.00')
        response = test_client.post('/employee/1/update',
                                    data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert request.url.endswith('/employee/1')
        assert db.session.query(Employee).get(1).first_name == 'BASIC_UPDATED'
        assert 'Employee information has been updated' in response.data.decode(
            'utf-8')

    def test_get_inactivate(self, test_client):
        response = test_client.get('/employee/1/inactivate')
        assert response.status_code == 405

    def test_post_inativate(self, test_client, test_employees):
        response = test_client.post('/employee/1/inactivate',
                                    follow_redirects=True)
        assert response.status_code == 200
        assert request.url.endswith('/employee/1')
        assert 'Employee has been inactivated' in response.data.decode(
            'utf-8')
        assert db.session.query(Employee).get(1).active == False

    def test_get_activate(self, test_client):
        response = test_client.get('/employee/1/activate')
        assert response.status_code == 405

    def test_post_ativate(self, test_client, test_employees):
        response = test_client.post('/employee/1/activate',
                                    follow_redirects=True)
        assert response.status_code == 200
        assert request.url.endswith('/employee/1')
        assert 'Employee has been activated' in response.data.decode(
            'utf-8')
        assert db.session.query(Employee).get(1).active == True


class TestUpload:
    def test_get(self, test_client, test_employees):
        response = test_client.get('/employee/1/upload')
        assert response.status_code == 405

    def test_invalid_post(self, test_client, test_employees):
        data = dict(
            file=(io.BytesIO(b'test'), "test.exe"),
        )
        response = test_client.post('/employee/1/upload',
                                    data=data,
                                    follow_redirects=True,
                                    content_type='multipart/form-data')
        assert response.status_code == 200
        assert 'Invalid File Format:' in response.data.decode('utf-8')

    def test_valid_post(self, test_client, test_employees):
        data = dict(
            file=(io.BytesIO(b'test'), "test_upload.pdf"),
        )
        response = test_client.post('/employee/1/upload',
                                    data=data,
                                    follow_redirects=True,
                                    content_type='multipart/form-data')
        assert response.status_code == 200
        f = db.session.query(File).get(1)
        assert f.full_name == "test_upload.pdf"
        assert os.path.isfile(f.file_path) == 1
