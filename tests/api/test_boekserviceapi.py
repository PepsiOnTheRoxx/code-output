from flask import Flask
from src.api.boekserviceapi import register_routes
from src.api import boekserviceapi
from src.api.boekserviceapi_exceptions import BoekNotFoundException, InvalidBoekDataException
import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def client():
    app = Flask(__name__)
    register_routes(app)
    return app.test_client()

def test_get_all_boeken_returns_list(client):
    boeken = [
        {"id": 1, "titel": "Boek 1", "auteur": "Auteur 1"},
        {"id": 2, "titel": "Boek 2", "auteur": "Auteur 2"}
    ]
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.get_all_boeken.return_value = boeken
        response = client.get("/boeken")
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == boeken

def test_get_boek_by_id_success(client):
    boek = {"id": 1, "titel": "Test boek", "auteur": "Auteur"}
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.get_boek_by_id.return_value = boek
        response = client.get("/boeken/1")
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == boek

def test_get_boek_by_id_not_found(client):
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.get_boek_by_id.side_effect = BoekNotFoundException("Niet gevonden")
        response = client.get("/boeken/999")
        assert response.status_code == 404
        assert response.is_json
        assert response.get_json()["error"] == "Niet gevonden"

def test_create_boek_success(client):
    boek_data = {"titel": "Nieuw Boek", "auteur": "Nieuwe Auteur"}
    boek_response = {"id": 3, "titel": "Nieuw Boek", "auteur": "Nieuwe Auteur"}
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.create_boek.return_value = boek_response
        response = client.post("/boeken", json=boek_data)
        assert response.status_code == 201
        assert response.is_json
        assert response.get_json() == boek_response

def test_create_boek_invalid_data(client):
    boek_data = {"titel": ""}
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.create_boek.side_effect = InvalidBoekDataException("Ongeldige data")
        response = client.post("/boeken", json=boek_data)
        assert response.status_code == 400
        assert response.is_json
        assert response.get_json()["error"] == "Ongeldige data"

def test_update_boek_success(client):
    boek_data = {"titel": "Aangepast Boek", "auteur": "Aangepast Auteur"}
    boek_response = {"id": 2, "titel": "Aangepast Boek", "auteur": "Aangepast Auteur"}
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.update_boek.return_value = boek_response
        response = client.put("/boeken/2", json=boek_data)
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == boek_response

def test_update_boek_not_found(client):
    boek_data = {"titel": "Onbekend"}
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.update_boek.side_effect = BoekNotFoundException("Niet gevonden")
        response = client.put("/boeken/999", json=boek_data)
        assert response.status_code == 404
        assert response.is_json
        assert response.get_json()["error"] == "Niet gevonden"

def test_update_boek_invalid_data(client):
    boek_data = {"titel": ""}
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.update_boek.side_effect = InvalidBoekDataException("Ongeldige data")
        response = client.put("/boeken/1", json=boek_data)
        assert response.status_code == 400
        assert response.is_json
        assert response.get_json()["error"] == "Ongeldige data"

def test_delete_boek_success(client):
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        response = client.delete("/boeken/1")
        instance.delete_boek.assert_called_once_with(1)
        assert response.status_code == 204
        assert response.data == b""

def test_delete_boek_not_found(client):
    with patch("src.api.boekserviceapi.BoekService", autospec=True) as MockBoekService:
        instance = MockBoekService.return_value
        instance.delete_boek.side_effect = BoekNotFoundException("Niet gevonden")
        response = client.delete("/boeken/999")
        assert response.status_code == 404
        assert response.is_json
        assert response.get_json()["error"] == "Niet gevonden"