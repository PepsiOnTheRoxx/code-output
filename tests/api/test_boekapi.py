import pytest
from flask import Flask, json
from unittest.mock import patch
from src.api import boekapi
from src.api.boekapi_exceptions import BoekAPINotFoundException as BoekNotFoundException, BoekAPIValidationException as BoekValidationException

@pytest.fixture
def client():
    app = Flask(__name__)
    boekapi.register_routes(app)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("src.api.boekapi.BoekService")
def test_create_boek_success(mock_service, client):
    boek_data = {"titel": "Testboek", "auteur": "Auteur A"}
    created_boek = {"id": 1, **boek_data}
    instance = mock_service.return_value
    instance.create_boek.return_value = created_boek

    response = client.post("/boeken", json=boek_data)

    assert response.status_code == 201
    assert response.get_json() == created_boek
    instance.create_boek.assert_called_once_with(boek_data)

@patch("src.api.boekapi.BoekService")
def test_create_boek_validation_error(mock_service, client):
    instance = mock_service.return_value
    instance.create_boek.side_effect = BoekValidationException("Titel ontbreekt")

    response = client.post("/boeken", json={})

    assert response.status_code == 400
    assert "Titel ontbreekt" in response.get_json()["error"]

@patch("src.api.boekapi.BoekService")
def test_read_boek_success(mock_service, client):
    boek = {"id": 1, "titel": "Testboek", "auteur": "Auteur A"}
    instance = mock_service.return_value
    instance.get_boek.return_value = boek

    response = client.get("/boeken/1")

    assert response.status_code == 200
    assert response.get_json() == boek
    instance.get_boek.assert_called_once_with(1)

@patch("src.api.boekapi.BoekService")
def test_read_boek_not_found(mock_service, client):
    instance = mock_service.return_value
    instance.get_boek.side_effect = BoekNotFoundException("Niet gevonden")

    response = client.get("/boeken/999")

    assert response.status_code == 404
    assert "Niet gevonden" in response.get_json()["error"]

@patch("src.api.boekapi.BoekService")
def test_update_boek_success(mock_service, client):
    updated_boek = {"id": 1, "titel": "Gewijzigd", "auteur": "Auteur B"}
    instance = mock_service.return_value
    instance.update_boek.return_value = updated_boek

    response = client.put("/boeken/1", json={"titel": "Gewijzigd", "auteur": "Auteur B"})

    assert response.status_code == 200
    assert response.get_json() == updated_boek
    instance.update_boek.assert_called_once_with(1, {"titel": "Gewijzigd", "auteur": "Auteur B"})

@patch("src.api.boekapi.BoekService")
def test_update_boek_not_found(mock_service, client):
    instance = mock_service.return_value
    instance.update_boek.side_effect = BoekNotFoundException("Niet gevonden")

    response = client.put("/boeken/999", json={"titel": "Test", "auteur": "Auteur"})

    assert response.status_code == 404
    assert "Niet gevonden" in response.get_json()["error"]

@patch("src.api.boekapi.BoekService")
def test_update_boek_validation_error(mock_service, client):
    instance = mock_service.return_value
    instance.update_boek.side_effect = BoekValidationException("Foutieve data")

    response = client.put("/boeken/1", json={})

    assert response.status_code == 400
    assert "Foutieve data" in response.get_json()["error"]

@patch("src.api.boekapi.BoekService")
def test_delete_boek_success(mock_service, client):
    instance = mock_service.return_value

    response = client.delete("/boeken/1")

    assert response.status_code == 204
    instance.delete_boek.assert_called_once_with(1)

@patch("src.api.boekapi.BoekService")
def test_delete_boek_not_found(mock_service, client):
    instance = mock_service.return_value
    instance.delete_boek.side_effect = BoekNotFoundException("Niet gevonden")

    response = client.delete("/boeken/999")

    assert response.status_code == 404
    assert "Niet gevonden" in response.get_json()["error"]

@patch("src.api.boekapi.BoekService")
def test_list_boeken_success(mock_service, client):
    boeken = [
        {"id": 1, "titel": "Boek1", "auteur": "A"},
        {"id": 2, "titel": "Boek2", "auteur": "B"}
    ]
    instance = mock_service.return_value
    instance.list_boeken.return_value = boeken

    response = client.get("/boeken")

    assert response.status_code == 200
    assert response.get_json() == boeken
    instance.list_boeken.assert_called_once()
