import pytest
from unittest.mock import patch, MagicMock
from src.api import gebruikerserviceapi
from src.api import gebruikerserviceapi_exceptions

@pytest.fixture
def client():
    with patch("src.api.gebruikerserviceapi.Flask") as mock_flask:
        app = MagicMock()
        app.test_client.return_value = MagicMock()
        mock_flask.return_value = app
        yield app.test_client.return_value

def test_get_gebruiker_success(client):
    gebruikers_data = {"id": 1, "naam": "jan"}
    with patch("src.api.gebruikerserviceapi.GebruikerService") as MockService:
        instance = MockService.return_value
        instance.get_gebruiker.return_value = gebruikers_data
        with patch("src.api.gebruikerserviceapi.jsonify", side_effect=lambda x: x) as mock_jsonify:
            response = gebruikerserviceapi.get_gebruiker(1)
            assert response == gebruikers_data
            instance.get_gebruiker.assert_called_once_with(1)

def test_get_gebruiker_not_found(client):
    with patch("src.api.gebruikerserviceapi.GebruikerService") as MockService:
        instance = MockService.return_value
        instance.get_gebruiker.side_effect = gebruikerserviceapi_exceptions.GebruikerNotFoundException()
        with pytest.raises(gebruikerserviceapi_exceptions.GebruikerNotFoundException):
            gebruikerserviceapi.get_gebruiker(1)

def test_post_gebruiker_success(client):
    data = {"naam": "piet"}
    created_user = {"id": 2, "naam": "piet"}
    with patch("src.api.gebruikerserviceapi.request") as mock_request, \
         patch("src.api.gebruikerserviceapi.GebruikerService") as MockService, \
         patch("src.api.gebruikerserviceapi.jsonify", side_effect=lambda x: x):
        mock_request.get_json.return_value = data
        instance = MockService.return_value
        instance.create_gebruiker.return_value = created_user
        response = gebruikerserviceapi.create_gebruiker()
        assert response == created_user
        instance.create_gebruiker.assert_called_once_with(data)

def test_post_gebruiker_invalid_data(client):
    with patch("src.api.gebruikerserviceapi.request") as mock_request, \
         patch("src.api.gebruikerserviceapi.GebruikerService") as MockService:
        mock_request.get_json.return_value = {}
        instance = MockService.return_value
        instance.create_gebruiker.side_effect = gebruikerserviceapi_exceptions.GebruikerValidationException("Invalid data")
        with pytest.raises(gebruikerserviceapi_exceptions.GebruikerValidationException):
            gebruikerserviceapi.create_gebruiker()

def test_delete_gebruiker_success(client):
    with patch("src.api.gebruikerserviceapi.GebruikerService") as MockService, \
         patch("src.api.gebruikerserviceapi.jsonify", side_effect=lambda x: x):
        instance = MockService.return_value
        instance.delete_gebruiker.return_value = True
        response = gebruikerserviceapi.delete_gebruiker(3)
        assert response is True
        instance.delete_gebruiker.assert_called_once_with(3)

def test_delete_gebruiker_not_found(client):
    with patch("src.api.gebruikerserviceapi.GebruikerService") as MockService:
        instance = MockService.return_value
        instance.delete_gebruiker.side_effect = gebruikerserviceapi_exceptions.GebruikerNotFoundException()
        with pytest.raises(gebruikerserviceapi_exceptions.GebruikerNotFoundException):
            gebruikerserviceapi.delete_gebruiker(4)