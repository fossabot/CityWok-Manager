from citywok_ms import db
from citywok_ms.models import Employee
from flask import request


def test_get_update(test_client, test_employees):
    response = test_client.get('/employee/1/update')
    assert response.status_code == 200
    assert b'Update employee information' in response.data
    assert b'Update' in response.data
    assert b'TEST_1' in response.data
    assert b'INFO' in response.data


def test_post_update(test_client, test_employees):
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


def test_get_inactivate(test_client):
    response = test_client.get('/employee/1/inactivate')
    assert response.status_code == 405


def test_post_inativate(test_client, test_employees):
    response = test_client.post('/employee/1/inactivate',
                                follow_redirects=True)
    assert response.status_code == 200
    assert request.url.endswith('/employee/1')
    assert 'Employee has been inactivated' in response.data.decode(
        'utf-8')
    assert db.session.query(Employee).get(1).active == False


def test_get_activate(test_client):
    response = test_client.get('/employee/1/activate')
    assert response.status_code == 405


def test_post_ativate(test_client, test_employees):
    response = test_client.post('/employee/1/activate',
                                follow_redirects=True)
    assert response.status_code == 200
    assert request.url.endswith('/employee/1')
    assert 'Employee has been activated' in response.data.decode(
        'utf-8')
    assert db.session.query(Employee).get(1).active == True
