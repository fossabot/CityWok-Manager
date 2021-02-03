from re import S
from citywok_ms import db
from citywok_ms.models import Supplier
from flask import request


class TestNew:
    def test_get(self, test_client):
        response = test_client.get('/supplier/new')
        assert response.status_code == 200
        assert b"New Supplier" in response.data

    def test_full_info(self, test_client):
        data = dict(name='FULL_INFO',
                    abbreviation='F_I',
                    principal='abc',
                    contact='123123123',
                    email='123@mail.com',
                    nif='123123',
                    iban='PT50123123',
                    address='rua A',
                    postcode='1234-567',
                    city='city',
                    remark='REMARK')
        response = test_client.post('/supplier/new',
                                    data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert request.url.endswith('/supplier/')
        assert 'Successfully' in response.data.decode('utf-8')
        assert 'This field is required' not in response.data.decode('utf-8')

        assert len(db.session.query(Supplier).filter_by(
            name="FULL_INFO").all()) == 1

    def test_basic_info(self, test_client):
        data = dict(name='BASIC_INFO',
                    principal='abc')
        response = test_client.post('/supplier/new',
                                    data=data,
                                    follow_redirects=True)

        assert response.status_code == 200
        assert request.url.endswith('/supplier/')
        assert 'Successfully' in response.data.decode('utf-8')
        assert 'This field is required' not in response.data.decode('utf-8')

        assert len(db.session.query(Supplier).all()) == 2

        assert len(db.session.query(Supplier).filter_by(
            name="BASIC_INFO").all()) == 1

    def test_empty(self, test_client):
        response = test_client.post('/supplier/new',
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'This field is required' in response.data.decode('utf-8')
        assert 'Successfully' not in response.data.decode('utf-8')
        assert len(db.session.query(Supplier).all()) == 2

    def test_duplicate_nif(self, test_client):
        data = dict(name='BASIC_INFO',
                    nif='123123',
                    principal='abc')
        response = test_client.post('/supplier/new',
                                    data=data,
                                    follow_redirects=True)

        assert response.status_code == 200
        assert 'This NIF already existe' in response.data.decode('utf-8')
        assert 'Successfully' not in response.data.decode('utf-8')
        assert len(db.session.query(Supplier).all()) == 2

    def test_duplicate_iban(self, test_client):
        data = dict(name='BASIC_INFO',
                    iban='PT50123123',
                    principal='abc')
        response = test_client.post('/supplier/new',
                                    data=data,
                                    follow_redirects=True)

        assert response.status_code == 200
        assert 'This IBAN already existe' in response.data.decode('utf-8')
        assert 'Successfully' not in response.data.decode('utf-8')
        assert len(db.session.query(Supplier).all()) == 2


class TestIndex:
    def test_get(self, test_client):
        response = test_client.get('/supplier/')
        assert response.status_code == 200
        assert b'Suppliers' in response.data

    def test_supplier_data(self, test_client, test_suppliers):
        response = test_client.get('/supplier/')
        assert response.status_code == 200
        assert b'TEST_1' in response.data
        assert b'TEST_2' in response.data

    def test_new_btn(self, test_client):
        response = test_client.get('/supplier/')
        assert response.status_code == 200
        assert b'/supplier/new' in response.data
        assert b'New' in response.data

    def test_detail_btn(self, test_client, test_suppliers):
        response = test_client.get('/supplier/')
        assert response.status_code == 200
        assert b'/supplier/1' in response.data
        assert b'/supplier/2' in response.data
        assert b'/supplier/4' not in response.data


class TestDetail:
    def test_get_valide(self, test_client, test_suppliers):
        response = test_client.get('/supplier/1')
        assert response.status_code == 200
        assert b'TEST_1' in response.data
        assert b'Supplier Detail' in response.data

        response = test_client.get('/supplier/2')
        assert response.status_code == 200
        assert b'TEST_2' in response.data
        assert b'Supplier Detail' in response.data

    def test_get_invalide(self, test_client, test_suppliers):
        response = test_client.get('/supplier/101')
        assert response.status_code == 404


class TestUpdate:
    def test_get_update(self, test_client, test_suppliers):
        response = test_client.get('/supplier/1/update')
        assert response.status_code == 200
        assert b'Update supplier' in response.data
        assert b'Update' in response.data
        assert b'TEST_1' in response.data
        assert b'P_1' in response.data

    def test_post_update(self, test_client, test_suppliers):
        data = dict(name='UPDATE_INFO',
                    abbreviation='U_I',
                    principal='abc',
                    contact='123123123',
                    email='123@mail.com',
                    nif='123123',
                    iban='PT50123123',
                    address='rua A',
                    postcode='1234-567',
                    city='city',
                    remark='REMARK')
        response = test_client.post('/supplier/1/update',
                                    data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert request.url.endswith('/supplier/1')
        assert db.session.query(Supplier).get(1).name == 'UPDATE_INFO'
        assert 'Supplier information has been updated' in response.data.decode(
            'utf-8')
