import pytest
from unittest.mock import patch, MagicMock
from src.api.boekserviceapi import app
from src.api.boekserviceapi_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

@patch("src.api.boekserviceapi.boek_service")
def test_creeer_boek_succes(mock_boek_service, client):
    boek_data = {"titel": "Testboek", "auteur": "Auteur X"}
    mock_boek_service.creeer_boek.return_value = {"id": 1, "titel": "Testboek", "auteur": "Auteur X"}
    response = client.post("/boeken", json=boek_data)
    assert response.status_code == 201
    assert response.json == {"id": 1, "titel": "Testboek", "auteur": "Auteur X"}
    mock_boek_service.creeer_boek.assert_called_once_with(boek_data)

@patch("src.api.boekserviceapi.boek_service")
def test_creeer_boek_ongeldige_data(mock_boek_service, client):
    boek_data = {"titel": ""}
    mock_boek_service.creeer_boek.side_effect = OngeldigeBoekDataException("Ongeldige data")
    response = client.post("/boeken", json=boek_data)
    assert response.status_code == 400
    assert "Ongeldige data" in response.json["beschrijving"]
    mock_boek_service.creeer_boek.assert_called_once_with(boek_data)

@patch("src.api.boekserviceapi.boek_service")
def test_lees_boek_succes(mock_boek_service, client):
    mock_boek_service.lees_boek.return_value = {"id": 42, "titel": "Leesboek", "auteur": "Schrijver Z"}
    response = client.get("/boeken/42")
    assert response.status_code == 200
    assert response.json == {"id": 42, "titel": "Leesboek", "auteur": "Schrijver Z"}
    mock_boek_service.lees_boek.assert_called_once_with(42)

@patch("src.api.boekserviceapi.boek_service")
def test_lees_boek_niet_gevonden(mock_boek_service, client):
    mock_boek_service.lees_boek.side_effect = BoekNietGevondenException("Niet gevonden")
    response = client.get("/boeken/999")
    assert response.status_code == 404
    assert "Niet gevonden" in response.json["beschrijving"]
    mock_boek_service.lees_boek.assert_called_once_with(999)

@patch("src.api.boekserviceapi.boek_service")
def test_update_boek_succes(mock_boek_service, client):
    boek_data = {"titel": "Nieuw titel"}
    mock_boek_service.update_boek.return_value = {"id": 5, "titel": "Nieuw titel", "auteur": "Auteur Y"}
    response = client.put("/boeken/5", json=boek_data)
    assert response.status_code == 200
    assert response.json == {"id": 5, "titel": "Nieuw titel", "auteur": "Auteur Y"}
    mock_boek_service.update_boek.assert_called_once_with(5, boek_data)

@patch("src.api.boekserviceapi.boek_service")
def test_update_boek_niet_gevonden(mock_boek_service, client):
    boek_data = {"titel": "Onbekend"}
    mock_boek_service.update_boek.side_effect = BoekNietGevondenException("Boek niet gevonden")
    response = client.put("/boeken/999", json=boek_data)
    assert response.status_code == 404
    assert "Boek niet gevonden" in response.json["beschrijving"]
    mock_boek_service.update_boek.assert_called_once_with(999, boek_data)

@patch("src.api.boekserviceapi.boek_service")
def test_update_boek_ongeldige_data(mock_boek_service, client):
    boek_data = {"titel": ""}
    mock_boek_service.update_boek.side_effect = OngeldigeBoekDataException("Ongeldige update")
    response = client.put("/boeken/3", json=boek_data)
    assert response.status_code == 400
    assert "Ongeldige update" in response.json["beschrijving"]
    mock_boek_service.update_boek.assert_called_once_with(3, boek_data)

@patch("src.api.boekserviceapi.boek_service")
def test_verwijder_boek_succes(mock_boek_service, client):
    response = client.delete("/boeken/6")
    assert response.status_code == 204
    mock_boek_service.verwijder_boek.assert_called_once_with(6)

@patch("src.api.boekserviceapi.boek_service")
def test_verwijder_boek_niet_gevonden(mock_boek_service, client):
    mock_boek_service.verwijder_boek.side_effect = BoekNietGevondenException("Boek niet gevonden")
    response = client.delete("/boeken/111")
    assert response.status_code == 404
    assert "Boek niet gevonden" in response.json["beschrijving"]
    mock_boek_service.verwijder_boek.assert_called_once_with(111)
