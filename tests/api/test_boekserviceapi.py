from flask import Flask
from unittest.mock import patch, MagicMock
import pytest
from src.api.boekserviceapi import register_routes
from src.api.boekserviceapi_exceptions import BoekAPINotFoundException
import sys
import types

@pytest.fixture
def client():
    sys.modules['src.api'] = types.ModuleType('src.api')
    sys.modules['src.api.boekservice'] = types.ModuleType('src.api.boekservice')
    class DummyBoekService:
        def __init__(self, conn):
            pass
        def get_all_boeken(self):
            return []
        def get_boek(self, boek_id):
            return None
        def create_boek(self, data):
            return data
        def update_boek(self, boek_id, data):
            return data
        def delete_boek(self, boek_id):
            pass
    sys.modules['src.api.boekservice'].BoekService = DummyBoekService

    app = Flask(__name__)
    register_routes(app)
    return app.test_client(), app

def test_get_boek_returns_200_and_json(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.get_boek.return_value = {"id": 1, "titel": "Titel", "auteur": "Auteur"}
        app._test_boekservice_instance = mock_instance
        response = client.get("/boeken/1")
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"id": 1, "titel": "Titel", "auteur": "Auteur"}
        mock_instance.get_boek.assert_called_once_with(1)
        delattr(app, '_test_boekservice_instance')

def test_get_boek_not_found_returns_404(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.get_boek.side_effect = BoekAPINotFoundException()
        app._test_boekservice_instance = mock_instance
        response = client.get("/boeken/999")
        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()
        mock_instance.get_boek.assert_called_once_with(999)
        delattr(app, '_test_boekservice_instance')

def test_post_boek_returns_201_and_json(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.create_boek.return_value = {"id": 5, "titel": "Nieuw", "auteur": "Auteur"}
        app._test_boekservice_instance = mock_instance
        payload = {"titel": "Nieuw", "auteur": "Auteur"}
        response = client.post("/boeken", json=payload)
        assert response.status_code == 201
        assert response.is_json
        assert response.get_json() == {"id": 5, "titel": "Nieuw", "auteur": "Auteur"}
        mock_instance.create_boek.assert_called_once_with(payload)
        delattr(app, '_test_boekservice_instance')

def test_put_boek_returns_200_and_json(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.update_boek.return_value = {"id": 2, "titel": "Bewerkt", "auteur": "Auteur"}
        app._test_boekservice_instance = mock_instance
        payload = {"titel": "Bewerkt", "auteur": "Auteur"}
        response = client.put("/boeken/2", json=payload)
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"id": 2, "titel": "Bewerkt", "auteur": "Auteur"}
        mock_instance.update_boek.assert_called_once_with(2, payload)
        delattr(app, '_test_boekservice_instance')

def test_put_boek_not_found_returns_404(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.update_boek.side_effect = BoekAPINotFoundException()
        app._test_boekservice_instance = mock_instance
        payload = {"titel": "Niet bestaand", "auteur": "Auteur"}
        response = client.put("/boeken/404", json=payload)
        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()
        mock_instance.update_boek.assert_called_once_with(404, payload)
        delattr(app, '_test_boekservice_instance')

def test_delete_boek_returns_204(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        app._test_boekservice_instance = mock_instance
        response = client.delete("/boeken/3")
        assert response.status_code == 204
        mock_instance.delete_boek.assert_called_once_with(3)
        delattr(app, '_test_boekservice_instance')

def test_delete_boek_not_found_returns_404(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.delete_boek.side_effect = BoekAPINotFoundException()
        app._test_boekservice_instance = mock_instance
        response = client.delete("/boeken/888")
        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()
        mock_instance.delete_boek.assert_called_once_with(888)
        delattr(app, '_test_boekservice_instance')

def test_get_all_boeken_returns_200_and_json(client):
    client, app = client
    with patch("src.api.boekservice.BoekService") as MockService:
        mock_instance = MockService.return_value
        boeken_data = [
            {"id": 1, "titel": "Boek1", "auteur": "Auteur1"},
            {"id": 2, "titel": "Boek2", "auteur": "Auteur2"}
        ]
        mock_instance.get_all_boeken.return_value = boeken_data
        app._test_boekservice_instance = mock_instance
        response = client.get("/boeken")
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == boeken_data
        mock_instance.get_all_boeken.assert_called_once()
        delattr(app, '_test_boekservice_instance')
