import pytest
from unittest.mock import patch, MagicMock
from src.api import boekapi
from src.api.boekapi_exceptions import BoekNotFoundException, BoekValidationException

@pytest.fixture
def test_client():
    with patch("src.api.boekapi.app.test_client") as test_client_factory:
        client_mock = MagicMock()
        test_client_factory.return_value = client_mock
        yield client_mock

def test_get_boeken_success(test_client):
    boeken = [{"id": 1, "titel": "Testboek", "auteur": "Auteur A"}]
    with patch("src.api.boekapi.BoekService.get_all_boeken", return_value=boeken):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.get_json.return_value = boeken
        test_client.get.return_value = response_mock

        resp = boekapi.app.test_client().get("/boeken")

        assert resp.status_code == 200
        assert resp.get_json() == boeken

def test_get_boek_by_id_success(test_client):
    boek = {"id": 2, "titel": "Boek 2", "auteur": "Auteur B"}
    with patch("src.api.boekapi.BoekService.get_boek_by_id", return_value=boek):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.get_json.return_value = boek
        test_client.get.return_value = response_mock

        resp = boekapi.app.test_client().get("/boeken/2")

        assert resp.status_code == 200
        assert resp.get_json() == boek

def test_get_boek_by_id_not_found(test_client):
    with patch("src.api.boekapi.BoekService.get_boek_by_id", side_effect=BoekNotFoundException):
        response_mock = MagicMock()
        response_mock.status_code = 404
        response_mock.get_json.return_value = {"error": "Boek niet gevonden"}
        test_client.get.return_value = response_mock

        resp = boekapi.app.test_client().get("/boeken/99")

        assert resp.status_code == 404
        assert resp.get_json() == {"error": "Boek niet gevonden"}

def test_create_boek_success(test_client):
    boek_data = {"titel": "Nieuw Boek", "auteur": "Auteur C"}
    created_boek = {"id": 3, "titel": "Nieuw Boek", "auteur": "Auteur C"}

    with patch("src.api.boekapi.BoekService.create_boek", return_value=created_boek):
        response_mock = MagicMock()
        response_mock.status_code = 201
        response_mock.get_json.return_value = created_boek
        test_client.post.return_value = response_mock

        resp = boekapi.app.test_client().post("/boeken", json=boek_data)

        assert resp.status_code == 201
        assert resp.get_json() == created_boek

def test_create_boek_invalid(test_client):
    boek_data = {"titel": ""}

    with patch("src.api.boekapi.BoekService.create_boek", side_effect=BoekValidationException("Ongeldige input")):
        response_mock = MagicMock()
        response_mock.status_code = 400
        response_mock.get_json.return_value = {"error": "Ongeldige input"}
        test_client.post.return_value = response_mock

        resp = boekapi.app.test_client().post("/boeken", json=boek_data)

        assert resp.status_code == 400
        assert resp.get_json() == {"error": "Ongeldige input"}

def test_update_boek_success(test_client):
    boek_update = {"titel": "Updated Titel"}
    updated_boek = {"id": 1, "titel": "Updated Titel", "auteur": "Auteur A"}

    with patch("src.api.boekapi.BoekService.update_boek", return_value=updated_boek):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.get_json.return_value = updated_boek
        test_client.put.return_value = response_mock

        resp = boekapi.app.test_client().put("/boeken/1", json=boek_update)

        assert resp.status_code == 200
        assert resp.get_json() == updated_boek

def test_update_boek_not_found(test_client):
    boek_update = {"titel": "Updated Titel"}

    with patch("src.api.boekapi.BoekService.update_boek", side_effect=BoekNotFoundException):
        response_mock = MagicMock()
        response_mock.status_code = 404
        response_mock.get_json.return_value = {"error": "Boek niet gevonden"}
        test_client.put.return_value = response_mock

        resp = boekapi.app.test_client().put("/boeken/99", json=boek_update)

        assert resp.status_code == 404
        assert resp.get_json() == {"error": "Boek niet gevonden"}

def test_update_boek_invalid(test_client):
    boek_update = {"titel": ""}

    with patch("src.api.boekapi.BoekService.update_boek", side_effect=BoekValidationException("Ongeldige data")):
        response_mock = MagicMock()
        response_mock.status_code = 400
        response_mock.get_json.return_value = {"error": "Ongeldige data"}
        test_client.put.return_value = response_mock

        resp = boekapi.app.test_client().put("/boeken/1", json=boek_update)

        assert resp.status_code == 400
        assert resp.get_json() == {"error": "Ongeldige data"}

def test_delete_boek_success(test_client):
    with patch("src.api.boekapi.BoekService.delete_boek", return_value=None):
        response_mock = MagicMock()
        response_mock.status_code = 204
        response_mock.data = b""
        test_client.delete.return_value = response_mock

        resp = boekapi.app.test_client().delete("/boeken/1")

        assert resp.status_code == 204
        assert resp.data == b""

def test_delete_boek_not_found(test_client):
    with patch("src.api.boekapi.BoekService.delete_boek", side_effect=BoekNotFoundException):
        response_mock = MagicMock()
        response_mock.status_code = 404
        response_mock.get_json.return_value = {"error": "Boek niet gevonden"}
        test_client.delete.return_value = response_mock

        resp = boekapi.app.test_client().delete("/boeken/99")

        assert resp.status_code == 404
        assert resp.get_json() == {"error": "Boek niet gevonden"}