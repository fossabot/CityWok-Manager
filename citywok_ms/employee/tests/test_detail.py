def test_get_valide(test_client, test_employees):
    response = test_client.get('/employee/1')
    assert response.status_code == 200
    assert b'TEST_1 INFO' in response.data
    assert b'Employee Detail' in response.data

    response = test_client.get('/employee/2')
    assert response.status_code == 200
    assert b'TEST_2 INFO' in response.data
    assert b'Employee Detail' in response.data


def test_get_invalide(test_client, test_employees):
    response = test_client.get('/employee/101')
    assert response.status_code == 404


def test_activate_btns(test_client, test_employees):
    response = test_client.get('/employee/1')
    assert response.status_code == 200
    assert b'employee/1/update' in response.data
    assert b'employee/1/inactivate' in response.data
    assert b'employee/1/activate' not in response.data
    assert b'Inactive' not in response.data


def test_inactivate_btns(test_client, test_employees):
    response = test_client.get('/employee/3')
    assert response.status_code == 200

    assert b'employee/3/update' in response.data
    assert b'employee/3/activate' in response.data
    assert b'employee/3/inactivate' not in response.data
    assert b'Inactive' in response.data
