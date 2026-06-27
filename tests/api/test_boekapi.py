import pytest
from flask import Flask, json
from unittest.mock import patch, MagicMock
from src.api import boekapi
from src.api.boekapi_exceptions import BoekNotFoundException, InvalidBoekDataException

@pytest.fixture
def client():
    app = Flask(__name__)
    boekapi.register_routes(app)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def boek_data():
    return {
        "auteur": "Auteur Naam",
        "beschrijving": "Beschrijving van het boek",
        "isbn": "9781234567890",
        "publicatiedatum": "2023-05-01",
        "kaft_foto_url": "https://voorbeeld.nl/kaft.jpg",
        "is_uitgeleend": False,
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }

def test_get_all_boeken(client):
    boeken_list = [
        {
            "auteur": "Auteur 1",
            "beschrijving": "Boek 1",
            "isbn": "1111111111",
            "publicatiedatum": "2022-09-10",
            "kaft_foto_url": "https://img.com/1.jpg",
            "is_uitgeleend": False,
            "uitgeleend_datum": None,
            "uitgeleend_max_tot": None
        },
        {
            "auteur": "Auteur 2",
            "beschrijving": "Boek 2",
            "isbn": "2222222222",
            "publicatiedatum": "2021-07-12",
            "kaft_foto_url": "https://img.com/2.jpg",
            "is_uitgeleend": True,
            "uitgeleend_datum": "2023-01-05",
            "uitgeleend_max_tot": "2023-01-20"
        }
    ]
    with patch("src.api.boekapi.get_all_boeken", return_value=boeken_list):
        resp = client.get("/boeken")
        assert resp.status_code == 200
        assert resp.get_json() == boeken_list

def test_get_boek_by_isbn_success(client, boek_data):
    with patch("src.api.boekapi.get_boek_by_isbn", return_value=boek_data):
        resp = client.get(f"/boeken/{boek_data['isbn']}")
        assert resp.status_code == 200
        assert resp.get_json() == boek_data

def test_get_boek_by_isbn_not_found(client):
    with patch("src.api.boekapi.get_boek_by_isbn", side_effect=BoekNotFoundException()):
        resp = client.get("/boeken/9789999999999")
        assert resp.status_code == 404

def test_create_boek_success(client, boek_data):
    with patch("src.api.boekapi.create_boek", return_value=boek_data) as mock_create:
        resp = client.post("/boeken", data=json.dumps(boek_data), content_type="application/json")
        assert resp.status_code == 201
        assert resp.get_json() == boek_data
        mock_create.assert_called_once_with(boek_data)

def test_create_boek_invalid_data(client, boek_data):
    with patch("src.api.boekapi.create_boek", side_effect=InvalidBoekDataException()):
        resp = client.post("/boeken", data=json.dumps(boek_data), content_type="application/json")
        assert resp.status_code == 400

def test_update_boek_success(client, boek_data):
    updated_data = boek_data.copy()
    updated_data["beschrijving"] = "Nieuwe beschrijving"
    with patch("src.api.boekapi.update_boek", return_value=updated_data) as mock_update:
        resp = client.put(f"/boeken/{boek_data['isbn']}", data=json.dumps(updated_data), content_type="application/json")
        assert resp.status_code == 200
        assert resp.get_json() == updated_data
        mock_update.assert_called_once_with(boek_data['isbn'], updated_data)

def test_update_boek_not_found(client, boek_data):
    with patch("src.api.boekapi.update_boek", side_effect=BoekNotFoundException()):
        resp = client.put(f"/boeken/{boek_data['isbn']}", data=json.dumps(boek_data), content_type="application/json")
        assert resp.status_code == 404

def test_delete_boek_success(client, boek_data):
    with patch("src.api.boekapi.delete_boek", return_value=True) as mock_del:
        resp = client.delete(f"/boeken/{boek_data['isbn']}")
        assert resp.status_code == 204
        mock_del.assert_called_once_with(boek_data['isbn'])

def test_delete_boek_not_found(client, boek_data):
    with patch("src.api.boekapi.delete_boek", side_effect=BoekNotFoundException()):
        resp = client.delete(f"/boeken/{boek_data['isbn']}")
        assert resp.status_code == 404