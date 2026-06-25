import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from src.api.boekserviceapi import register_routes
from src.api.boekserviceapi_exceptions import BoekNotFoundException, InvalidBoekDataException

@pytest.fixture
def client():
    app = Flask(__name__)
    register_routes(app)
    with app.test_client() as client:
        yield client

@patch('src.api.boekserviceapi.BoekService')
def test_get_boek_success(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.get_boek.return_value = {'id': 1, 'titel': 'Testboek'}
    mock_service_class.return_value = mock_service

    response = client.get('/boeken/1')

    assert response.status_code == 200
    assert response.get_json() == {'id': 1, 'titel': 'Testboek'}
    mock_service.get_boek.assert_called_once_with(1)

@patch('src.api.boekserviceapi.BoekService')
def test_get_boek_not_found(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.get_boek.side_effect = BoekNotFoundException()
    mock_service_class.return_value = mock_service

    response = client.get('/boeken/999')

    assert response.status_code == 404
    assert response.get_json()['error'] == 'Boek niet gevonden'

@patch('src.api.boekserviceapi.BoekService')
def test_create_boek_success(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.create_boek.return_value = {'id': 2, 'titel': 'Nieuw Boek'}
    mock_service_class.return_value = mock_service

    response = client.post('/boeken', json={'titel': 'Nieuw Boek'})

    assert response.status_code == 201
    assert response.get_json() == {'id': 2, 'titel': 'Nieuw Boek'}
    mock_service.create_boek.assert_called_once_with({'titel': 'Nieuw Boek'})

@patch('src.api.boekserviceapi.BoekService')
def test_create_boek_invalid_data(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.create_boek.side_effect = InvalidBoekDataException('Titel ontbreekt')
    mock_service_class.return_value = mock_service

    response = client.post('/boeken', json={})

    assert response.status_code == 400
    assert "ontbreekt" in response.get_json()['error']

@patch('src.api.boekserviceapi.BoekService')
def test_update_boek_success(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.update_boek.return_value = {'id': 3, 'titel': 'Gewijzigd Boek'}
    mock_service_class.return_value = mock_service

    response = client.put('/boeken/3', json={'titel': 'Gewijzigd Boek'})

    assert response.status_code == 200
    assert response.get_json() == {'id': 3, 'titel': 'Gewijzigd Boek'}
    mock_service.update_boek.assert_called_once_with(3, {'titel': 'Gewijzigd Boek'})

@patch('src.api.boekserviceapi.BoekService')
def test_update_boek_not_found(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.update_boek.side_effect = BoekNotFoundException()
    mock_service_class.return_value = mock_service

    response = client.put('/boeken/1234', json={'titel': 'X'})

    assert response.status_code == 404
    assert response.get_json()['error'] == 'Boek niet gevonden'

@patch('src.api.boekserviceapi.BoekService')
def test_delete_boek_success(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.delete_boek.return_value = None
    mock_service_class.return_value = mock_service

    response = client.delete('/boeken/5')

    assert response.status_code == 204
    assert response.data == b''
    mock_service.delete_boek.assert_called_once_with(5)

@patch('src.api.boekserviceapi.BoekService')
def test_delete_boek_not_found(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.delete_boek.side_effect = BoekNotFoundException()
    mock_service_class.return_value = mock_service

    response = client.delete('/boeken/55')

    assert response.status_code == 404
    assert response.get_json()['error'] == 'Boek niet gevonden'

@patch('src.api.boekserviceapi.BoekService')
def test_get_all_boeken_success(mock_service_class, client):
    mock_service = MagicMock()
    mock_service.get_all_boeken.return_value = [
        {'id': 1, 'titel': 'Boek 1'},
        {'id': 2, 'titel': 'Boek 2'}
    ]
    mock_service_class.return_value = mock_service

    response = client.get('/boeken')

    assert response.status_code == 200
    assert response.get_json() == [
        {'id': 1, 'titel': 'Boek 1'},
        {'id': 2, 'titel': 'Boek 2'}
    ]
    mock_service.get_all_boeken.assert_called_once_with()