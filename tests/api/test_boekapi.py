import pytest
from unittest.mock import MagicMock
from src.api import boekapi
from src.api import boekapi_exceptions
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    service = MagicMock()
    boekapi.register_routes(app, service=service)
    app.mockservice = service
    with app.test_client() as client:
        client.mockservice = service
        yield client

def test_get_all_boeken_success(client):
    mock_boeken = [
        {'id': 1, 'titel': 'Test Boek 1'},
        {'id': 2, 'titel': 'Test Boek 2'}
    ]
    client.mockservice.get_all_boeken.return_value = mock_boeken
    response = client.get("/boeken")
    assert response.status_code == 200
    assert response.json == mock_boeken

def test_get_boek_by_id_success(client):
    mock_boek = {'id': 1, 'titel': 'Test Boek'}
    client.mockservice.get_boek_by_id.return_value = mock_boek
    response = client.get("/boeken/1")
    assert response.status_code == 200
    assert response.json == mock_boek

def test_get_boek_by_id_not_found(client):
    client.mockservice.get_boek_by_id.side_effect = boekapi_exceptions.BoekNotFoundException
    response = client.get("/boeken/999")
    assert response.status_code == 404
    assert "not found" in response.json["message"].lower()

def test_create_boek_success(client):
    input_data = {'titel': 'Nieuw Boek'}
    created_boek = {'id': 42, 'titel': 'Nieuw Boek'}
    client.mockservice.create_boek.return_value = created_boek
    response = client.post("/boeken", json=input_data)
    assert response.status_code == 201
    assert response.json == created_boek

def test_create_boek_invalid_data(client):
    input_data = {'titel': ''}
    client.mockservice.create_boek.side_effect = boekapi_exceptions.BoekValidationException("Titel verplicht")
    response = client.post("/boeken", json=input_data)
    assert response.status_code == 400
    assert "titel verplicht" in response.json["message"].lower()

def test_update_boek_success(client):
    update_data = {'titel': 'Gewijzigd Boek'}
    updated_boek = {'id': 1, 'titel': 'Gewijzigd Boek'}
    client.mockservice.update_boek.return_value = updated_boek
    response = client.put("/boeken/1", json=update_data)
    assert response.status_code == 200
    assert response.json == updated_boek

def test_update_boek_not_found(client):
    update_data = {'titel': 'Gewijzigd Boek'}
    client.mockservice.update_boek.side_effect = boekapi_exceptions.BoekNotFoundException
    response = client.put("/boeken/999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json["message"].lower()

def test_delete_boek_success(client):
    response = client.delete("/boeken/1")
    assert response.status_code == 204
    assert response.data == b""
    client.mockservice.delete_boek.assert_called_with(1)

def test_delete_boek_not_found(client):
    client.mockservice.delete_boek.side_effect = boekapi_exceptions.BoekNotFoundException
    response = client.delete("/boeken/999")
    assert response.status_code == 404
    assert "not found" in response.json["message"].lower()
