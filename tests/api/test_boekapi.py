import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from src.api.boekapi import register_routes
from src.api.boekapi_exceptions import BoekNotFoundException

@pytest.fixture
def client():
    app = Flask(__name__)
    register_routes(app)
    return app.test_client()

@patch('src.api.boekapi.BoekService')
def test_get_all_boeken_success(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.get_all_boeken.return_value = [
        {"id": 1, "titel": "Boek A"},
        {"id": 2, "titel": "Boek B"}
    ]
    mock_boek_service.return_value = mock_service_instance

    response = client.get('/boeken')
    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "titel": "Boek A"},
        {"id": 2, "titel": "Boek B"}
    ]

@patch('src.api.boekapi.BoekService')
def test_get_boek_by_id_success(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.get_boek_by_id.return_value = {"id": 1, "titel": "Boek X"}
    mock_boek_service.return_value = mock_service_instance

    response = client.get('/boeken/1')
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "titel": "Boek X"}

@patch('src.api.boekapi.BoekService')
def test_get_boek_by_id_not_found(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.get_boek_by_id.side_effect = BoekNotFoundException("Not found")
    mock_boek_service.return_value = mock_service_instance

    response = client.get('/boeken/1234')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}

@patch('src.api.boekapi.BoekService')
def test_create_boek_success(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.create_boek.return_value = {"id": 3, "titel": "Nieuw Boek"}
    mock_boek_service.return_value = mock_service_instance

    response = client.post('/boeken', json={"titel": "Nieuw Boek"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 3, "titel": "Nieuw Boek"}

@patch('src.api.boekapi.BoekService')
def test_update_boek_success(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.update_boek.return_value = {"id": 1, "titel": "Boek Gewijzigd"}
    mock_boek_service.return_value = mock_service_instance

    response = client.put('/boeken/1', json={"titel": "Boek Gewijzigd"})
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "titel": "Boek Gewijzigd"}

@patch('src.api.boekapi.BoekService')
def test_update_boek_not_found(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.update_boek.side_effect = BoekNotFoundException("Boek niet gevonden")
    mock_boek_service.return_value = mock_service_instance

    response = client.put('/boeken/999', json={"titel": "Niet bestaand"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "Boek niet gevonden"}

@patch('src.api.boekapi.BoekService')
def test_delete_boek_success(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.delete_boek.return_value = True
    mock_boek_service.return_value = mock_service_instance

    response = client.delete('/boeken/2')
    assert response.status_code == 204
    assert response.data == b''

@patch('src.api.boekapi.BoekService')
def test_delete_boek_not_found(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.delete_boek.side_effect = BoekNotFoundException("Bestaat niet")
    mock_boek_service.return_value = mock_service_instance

    response = client.delete('/boeken/404')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Bestaat niet"}

@patch('src.api.boekapi.BoekService')
def test_get_boek_interfaces_success(mock_boek_service, client):
    mock_service_instance = MagicMock()
    interfaces_data = [
        {"interface_id": 1, "type": "interface1"},
        {"interface_id": 2, "type": "interface2"},
    ]
    mock_service_instance.get_all_interfaces_for_boek.return_value = interfaces_data
    mock_boek_service.return_value = mock_service_instance

    response = client.get('/boeken/1/interfaces')
    assert response.status_code == 200
    assert response.get_json() == interfaces_data

@patch('src.api.boekapi.BoekService')
def test_get_boek_interfaces_not_found(mock_boek_service, client):
    mock_service_instance = MagicMock()
    mock_service_instance.get_all_interfaces_for_boek.side_effect = BoekNotFoundException("Niet gevonden")
    mock_boek_service.return_value = mock_service_instance

    response = client.get('/boeken/111/interfaces')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Niet gevonden"}