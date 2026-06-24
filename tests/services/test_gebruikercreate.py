import pytest
from unittest.mock import patch, MagicMock
from src.services.gebruikercreate import GebruikerService
from src.services.gebruikercreate_exceptions import (
    GebruikerAlreadyExistsException,
    InvalidGebruikerDataException,
    StorageException
)


def test_create_gebruiker_success():
    gebruiker_data = {"naam": "Jan", "email": "jan@example.com"}
    created_gebruiker = {"id": 1, "naam": "Jan", "email": "jan@example.com"}
    service = GebruikerService()
    with patch.object(service, "_bestaat_gebruiker", return_value=False):
        with patch.object(service, "_opslaan_gebruiker", return_value=created_gebruiker) as mock_opslaan:
            result = service.create(gebruiker_data)
            assert result == created_gebruiker
            mock_opslaan.assert_called_once_with(gebruiker_data)


def test_create_gebruiker_already_exists():
    gebruiker_data = {"naam": "Piet", "email": "piet@example.com"}
    service = GebruikerService()
    with patch.object(service, "_bestaat_gebruiker", return_value=True):
        with pytest.raises(GebruikerAlreadyExistsException):
            service.create(gebruiker_data)


def test_create_gebruiker_invalid_data():
    gebruiker_data = {"naam": "", "email": "geenemail"}
    service = GebruikerService()
    with patch.object(service, "_validate_gebruiker_data", side_effect=InvalidGebruikerDataException):
        with patch.object(service, "_bestaat_gebruiker", return_value=False):
            with pytest.raises(InvalidGebruikerDataException):
                service.create(gebruiker_data)


def test_create_gebruiker_storage_exception():
    gebruiker_data = {"naam": "Joris", "email": "joris@example.com"}
    service = GebruikerService()
    with patch.object(service, "_bestaat_gebruiker", return_value=False):
        with patch.object(service, "_opslaan_gebruiker", side_effect=StorageException):
            with pytest.raises(StorageException):
                service.create(gebruiker_data)
