import pytest
from unittest.mock import patch, MagicMock
from src.api import gebruikerserviceapi
from src.api import gebruikerserviceapi_exceptions

import types

class DummyRequest:
    def __init__(self, data):
        self._data = data
    def get_json(self, force=False, silent=False):
        return self._data

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
        instance.get_gebruiker.side_effect = gebruikerserviceapi_exceptions.GebruikerNietGevondenException()
        with pytest.raises(gebruikerserviceapi_exceptions.GebruikerNietGevondenException):
            gebruikerserviceapi.get_gebruiker(1)

def test_post_gebruiker_success(client):
    data = {"naam": "piet"}
    created_user = {"id": 2, "naam": "piet"}
    with patch("src.api.gebruikerserviceapi.GebruikerService") as MockService, \
         patch("src.api.gebruikerserviceapi.jsonify", side_effect=lambda x: x):
        instance = MockService.return_value
        instance.create_gebruiker.return_value = created_user
        # Patch the flask.request globally used in code
        original_request = gebruikerserviceapi.request
        gebruikerserviceapi.request = DummyRequest(data)
        try:
            response = gebruikerserviceapi.create_gebruiker()
            assert response == created_user
            instance.create_gebruiker.assert_called_once_with(data)
        finally:
            gebruikerserviceapi.request = original_request

def test_post_gebruiker_invalid_data(client):
    with patch("src.api.gebruikerserviceapi.GebruikerService") as MockService:
        data = {}
        instance = MockService.return_value
        instance.create_gebruiker.side_effect = gebruikerserviceapi_exceptions.OngeldigeGebruikerDataException("Invalid data")
        original_request = gebruikerserviceapi.request
        gebruikerserviceapi.request = DummyRequest(data)
        try:
            with pytest.raises(gebruikerserviceapi_exceptions.OngeldigeGebruikerDataException):
                gebruikerserviceapi.create_gebruiker()
        finally:
            gebruikerserviceapi.request = original_request

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
        instance.delete_gebruiker.side_effect = gebruikerserviceapi_exceptions.GebruikerNietGevondenException()
        with pytest.raises(gebruikerserviceapi_exceptions.GebruikerNietGevondenException):
            gebruikerserviceapi.delete_gebruiker(4)
