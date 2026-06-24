import pytest
from unittest.mock import patch, MagicMock
from src.api import bronserviceapi
import src.api.bronserviceapi_exceptions as bron_exceptions
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    bronserviceapi.register_routes(app)
    with app.test_client() as client:
        yield client

def test_get_bron_success(client):
    expected_result = {'bron_id': 1, 'name': 'BRON'}
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.get_bron.return_value = expected_result
        response = client.get('/bron/1')
        assert response.status_code == 200
        assert response.get_json() == expected_result
        instance.get_bron.assert_called_once_with(1)

def test_get_bron_not_found(client):
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.get_bron.side_effect = bron_exceptions.BronNotFoundException('Not found')
        response = client.get('/bron/9999')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Not found'

def test_create_bron_success(client):
    new_bron_data = {'name': 'New Bron'}
    created_bron = {'bron_id': 2, 'name': 'New Bron'}
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.create_bron.return_value = created_bron
        response = client.post('/bron', json=new_bron_data)
        assert response.status_code == 201
        assert response.get_json() == created_bron
        instance.create_bron.assert_called_once_with(new_bron_data)

def test_create_bron_conflict(client):
    new_bron_data = {'name': 'New Bron'}
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.create_bron.side_effect = bron_exceptions.BronAlreadyExistsException('Already exists')
        response = client.post('/bron', json=new_bron_data)
        assert response.status_code == 409
        assert response.get_json()['error'] == 'Already exists'

def test_update_bron_success(client):
    update_data = {'name': 'Updated Bron'}
    updated_bron = {'bron_id': 1, 'name': 'Updated Bron'}
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.update_bron.return_value = updated_bron
        response = client.put('/bron/1', json=update_data)
        assert response.status_code == 200
        assert response.get_json() == updated_bron
        instance.update_bron.assert_called_once_with(1, update_data)

def test_update_bron_not_found(client):
    update_data = {'name': 'Updated Bron'}
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.update_bron.side_effect = bron_exceptions.BronNotFoundException('Not found')
        response = client.put('/bron/9999', json=update_data)
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Not found'

def test_delete_bron_success(client):
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        response = client.delete('/bron/1')
        assert response.status_code == 204
        instance.delete_bron.assert_called_once_with(1)

def test_delete_bron_not_found(client):
    with patch('src.api.bronserviceapi.BronService') as MockService:
        instance = MockService.return_value
        instance.delete_bron.side_effect = bron_exceptions.BronNotFoundException('Bron niet gevonden')
        response = client.delete('/bron/9999')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Bron niet gevonden'
