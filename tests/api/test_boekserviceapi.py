from flask import Flask
from unittest.mock import patch, MagicMock
import pytest
from src.api.boekserviceapi import register_routes
from src.api.boekserviceapi_exceptions import BoekNotFoundException

@pytest.fixture
def client():
    app = Flask(__name__)
    register_routes(app)
    return app.test_client()

def test_get_boek_returns_200_and_json(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.get_boek.return_value = {"id": 1, "titel": "Titel", "auteur": "Auteur"}

        response = client.get("/boeken/1")

        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"id": 1, "titel": "Titel", "auteur": "Auteur"}
        mock_instance.get_boek.assert_called_once_with(1)

def test_get_boek_not_found_returns_404(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.get_boek.side_effect = BoekNotFoundException()

        response = client.get("/boeken/999")

        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()

def test_post_boek_returns_201_and_json(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.create_boek.return_value = {"id": 5, "titel": "Nieuw", "auteur": "Auteur"}

        payload = {"titel": "Nieuw", "auteur": "Auteur"}
        response = client.post("/boeken", json=payload)

        assert response.status_code == 201
        assert response.is_json
        assert response.get_json() == {"id": 5, "titel": "Nieuw", "auteur": "Auteur"}
        mock_instance.create_boek.assert_called_once_with(payload)

def test_put_boek_returns_200_and_json(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.update_boek.return_value = {"id": 2, "titel": "Bewerkt", "auteur": "Auteur"}

        payload = {"titel": "Bewerkt", "auteur": "Auteur"}
        response = client.put("/boeken/2", json=payload)

        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"id": 2, "titel": "Bewerkt", "auteur": "Auteur"}
        mock_instance.update_boek.assert_called_once_with(2, payload)

def test_put_boek_not_found_returns_404(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.update_boek.side_effect = BoekNotFoundException()

        payload = {"titel": "Niet bestaand", "auteur": "Auteur"}
        response = client.put("/boeken/404", json=payload)

        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()

def test_delete_boek_returns_204(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value

        response = client.delete("/boeken/3")

        assert response.status_code == 204
        mock_instance.delete_boek.assert_called_once_with(3)

def test_delete_boek_not_found_returns_404(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        mock_instance.delete_boek.side_effect = BoekNotFoundException()

        response = client.delete("/boeken/888")

        assert response.status_code == 404
        assert response.is_json
        assert "error" in response.get_json()

def test_get_all_boeken_returns_200_and_json(client):
    with patch("src.api.boekserviceapi.BoekService") as MockService:
        mock_instance = MockService.return_value
        boeken_data = [
            {"id": 1, "titel": "Boek1", "auteur": "Auteur1"},
            {"id": 2, "titel": "Boek2", "auteur": "Auteur2"}
        ]
        mock_instance.get_all_boeken.return_value = boeken_data

        response = client.get("/boeken")

        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == boeken_data
        mock_instance.get_all_boeken.assert_called_once()