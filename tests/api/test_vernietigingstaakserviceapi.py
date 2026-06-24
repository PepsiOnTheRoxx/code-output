import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json

from src.api.vernietigingstaakserviceapi import VernietigingstaakAPI
from src.api.vernietigingstaakserviceapi_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakDataException,
    UnauthorizedAccessException
)

@pytest.fixture
def client():
    app = Flask(__name__)
    api = VernietigingstaakAPI()
    api.register_routes(app)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_get_vernietigingstaak_success(mock_service, client):
    taak_id = "vt-1234"
    mock_vernietigingstaak = {"id": taak_id, "status": "in_behandeling"}
    instance = mock_service.return_value
    instance.get_vernietigingstaak.return_value = mock_vernietigingstaak

    response = client.get(f'/vernietigingstaken/{taak_id}')
    assert response.status_code == 200
    assert response.get_json() == mock_vernietigingstaak

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_get_vernietigingstaak_not_found(mock_service, client):
    taak_id = "vt-nonexistent"
    instance = mock_service.return_value
    instance.get_vernietigingstaak.side_effect = VernietigingstaakNotFoundException()

    response = client.get(f'/vernietigingstaken/{taak_id}')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Vernietigingstaak niet gevonden"

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_create_vernietigingstaak_success(mock_service, client):
    new_taak = {"document_id": "doc-111"}
    created_taak = {"id": "vt-5678", "document_id": "doc-111", "status": "aangevraagd"}
    instance = mock_service.return_value
    instance.create_vernietigingstaak.return_value = created_taak

    response = client.post('/vernietigingstaken', data=json.dumps(new_taak), content_type='application/json')
    assert response.status_code == 201
    assert response.get_json() == created_taak

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_create_vernietigingstaak_invalid_input(mock_service, client):
    invalid_taak = {}
    instance = mock_service.return_value
    instance.create_vernietigingstaak.side_effect = InvalidVernietigingstaakDataException()

    response = client.post('/vernietigingstaken', data=json.dumps(invalid_taak), content_type='application/json')
    assert response.status_code == 400
    assert response.get_json()["error"] == "Ongeldige vernietigingstaak data"

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_update_vernietigingstaak_success(mock_service, client):
    taak_id = "vt-2024"
    update_data = {"status": "voltooid"}
    updated_taak = {"id": taak_id, "status": "voltooid"}

    instance = mock_service.return_value
    instance.update_vernietigingstaak.return_value = updated_taak

    response = client.put(f'/vernietigingstaken/{taak_id}', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.get_json() == updated_taak

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_update_vernietigingstaak_not_found(mock_service, client):
    taak_id = "vt-missing"
    update_data = {"status": "geweigerd"}
    instance = mock_service.return_value
    instance.update_vernietigingstaak.side_effect = VernietigingstaakNotFoundException()

    response = client.put(f'/vernietigingstaken/{taak_id}', data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Vernietigingstaak niet gevonden"

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_delete_vernietigingstaak_success(mock_service, client):
    taak_id = "vt-del"
    instance = mock_service.return_value
    instance.delete_vernietigingstaak.return_value = None

    response = client.delete(f'/vernietigingstaken/{taak_id}')
    assert response.status_code == 204

@patch('src.api.vernietigingstaakserviceapi.VernietigingstaakService')
def test_delete_vernietigingstaak_unauthorized(mock_service, client):
    taak_id = "vt-unauth"
    instance = mock_service.return_value
    instance.delete_vernietigingstaak.side_effect = UnauthorizedAccessException()

    response = client.delete(f'/vernietigingstaken/{taak_id}')
    assert response.status_code == 403
    assert response.get_json()["error"] == "Geen toegang tot deze taak"