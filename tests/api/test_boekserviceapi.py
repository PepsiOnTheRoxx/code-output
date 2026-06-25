import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from src.api.boekserviceapi import register_routes
from src.api.boekserviceapi_exceptions import BoekNietGevondenException

@pytest.fixture
def client():
    app = Flask(__name__)
    register_routes(app)
    return app.test_client()

@patch('src.api.boekserviceapi.BoekService')
def test_get_boeken_list_success(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.get_all_boeken.return_value = [
        {"id": 1, "titel": "Boek1", "auteur": "Auteur1"},
        {"id": 2, "titel": "Boek2", "auteur": "Auteur2"}
    ]
    mock_boek_service.return_value = mock_service

    response = client.get('/api/boeken')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [
        {"id": 1, "titel": "Boek1", "auteur": "Auteur1"},
        {"id": 2, "titel": "Boek2", "auteur": "Auteur2"}
    ]

@patch('src.api.boekserviceapi.BoekService')
def test_get_boek_detail_success(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.get_boek_by_id.return_value = {"id": 1, "titel": "Boek1", "auteur": "Auteur1"}
    mock_boek_service.return_value = mock_service

    response = client.get('/api/boeken/1')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": 1, "titel": "Boek1", "auteur": "Auteur1"}

@patch('src.api.boekserviceapi.BoekService')
def test_get_boek_detail_not_found(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.get_boek_by_id.side_effect = BoekNietGevondenException()
    mock_boek_service.return_value = mock_service

    response = client.get('/api/boeken/99')
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["error"] == "Boek not found"

@patch('src.api.boekserviceapi.BoekService')
def test_post_boek_success(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.create_boek.return_value = {"id": 10, "titel": "Nieuw Boek", "auteur": "Nieuwe Auteur"}
    mock_boek_service.return_value = mock_service

    response = client.post('/api/boeken', json={"titel": "Nieuw Boek", "auteur": "Nieuwe Auteur"})
    assert response.status_code == 201
    assert response.is_json
    assert response.get_json() == {"id": 10, "titel": "Nieuw Boek", "auteur": "Nieuwe Auteur"}

@patch('src.api.boekserviceapi.BoekService')
def test_put_boek_success(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.update_boek.return_value = {"id": 5, "titel": "Aangepast Boek", "auteur": "Auteur X"}
    mock_boek_service.return_value = mock_service

    response = client.put('/api/boeken/5', json={"titel": "Aangepast Boek", "auteur": "Auteur X"})
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": 5, "titel": "Aangepast Boek", "auteur": "Auteur X"}

@patch('src.api.boekserviceapi.BoekService')
def test_put_boek_not_found(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.update_boek.side_effect = BoekNietGevondenException()
    mock_boek_service.return_value = mock_service

    response = client.put('/api/boeken/123', json={"titel": "Onbekend", "auteur": "X"})
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["error"] == "Boek not found"

@patch('src.api.boekserviceapi.BoekService')
def test_delete_boek_success(mock_boek_service, client):
    mock_service = MagicMock()
    mock_boek_service.return_value = mock_service

    response = client.delete('/api/boeken/9')
    assert response.status_code == 204
    assert response.data == b''

@patch('src.api.boekserviceapi.BoekService')
def test_delete_boek_not_found(mock_boek_service, client):
    mock_service = MagicMock()
    mock_service.delete_boek_by_id.side_effect = BoekNietGevondenException()
    mock_boek_service.return_value = mock_service

    response = client.delete('/api/boeken/404')
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["error"] == "Boek not found"
