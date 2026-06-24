import pytest
from unittest.mock import patch, MagicMock
from src.api.gebruikerserviceapi import (
    get_gebruiker,
    create_gebruiker,
    update_gebruiker,
    delete_gebruiker,
)
from src.api.gebruikerserviceapi_exceptions import (
    GebruikerNotFoundException,
    GebruikerAlreadyExistsException,
    GebruikerValidationException,
)

def test_get_gebruiker_success():
    gebruiker_data = {"id": 1, "naam": "Piet", "email": "piet@example.com"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.get_by_id.return_value = gebruiker_data
        result = get_gebruiker(1)
        assert result == gebruiker_data
        MockService.get_by_id.assert_called_once_with(1)

def test_get_gebruiker_not_found():
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.get_by_id.side_effect = GebruikerNotFoundException("Niet gevonden")
        with pytest.raises(GebruikerNotFoundException):
            get_gebruiker(999)

def test_create_gebruiker_success():
    nieuwe_gebruiker = {"naam": "Klaas", "email": "klaas@example.com"}
    opgeslagen_gebruiker = {"id": 2, "naam": "Klaas", "email": "klaas@example.com"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.create.return_value = opgeslagen_gebruiker
        result = create_gebruiker(nieuwe_gebruiker)
        assert result == opgeslagen_gebruiker
        MockService.create.assert_called_once_with(nieuwe_gebruiker)

def test_create_gebruiker_already_exists():
    nieuwe_gebruiker = {"naam": "Klaas", "email": "klaas@example.com"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.create.side_effect = GebruikerAlreadyExistsException("Bestaat al")
        with pytest.raises(GebruikerAlreadyExistsException):
            create_gebruiker(nieuwe_gebruiker)

def test_create_gebruiker_invalid():
    foute_gebruiker = {"naam": "", "email": "invalid-email"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.create.side_effect = GebruikerValidationException("Ongeldige invoer")
        with pytest.raises(GebruikerValidationException):
            create_gebruiker(foute_gebruiker)

def test_update_gebruiker_success():
    gebruiker_id = 1
    wijziging = {"email": "pietnieuwe@example.com"}
    updated_gebruiker = {"id": 1, "naam": "Piet", "email": "pietnieuwe@example.com"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.update.return_value = updated_gebruiker
        result = update_gebruiker(gebruiker_id, wijziging)
        assert result == updated_gebruiker
        MockService.update.assert_called_once_with(gebruiker_id, wijziging)

def test_update_gebruiker_not_found():
    gebruiker_id = 999
    wijziging = {"email": "nietbestaan@example.com"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.update.side_effect = GebruikerNotFoundException("Niet gevonden")
        with pytest.raises(GebruikerNotFoundException):
            update_gebruiker(gebruiker_id, wijziging)

def test_update_gebruiker_validation():
    gebruiker_id = 1
    wijziging = {"email": "geen-email"}
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.update.side_effect = GebruikerValidationException("Fout")
        with pytest.raises(GebruikerValidationException):
            update_gebruiker(gebruiker_id, wijziging)

def test_delete_gebruiker_success():
    gebruiker_id = 1
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.delete.return_value = True
        result = delete_gebruiker(gebruiker_id)
        assert result is True
        MockService.delete.assert_called_once_with(gebruiker_id)

def test_delete_gebruiker_not_found():
    gebruiker_id = 999
    with patch("src.api.gebruikerserviceapi._gebruiker_service_instance") as MockService:
        MockService.delete.side_effect = GebruikerNotFoundException("Niet gevonden")
        with pytest.raises(GebruikerNotFoundException):
            delete_gebruiker(gebruiker_id)
