import pytest
from unittest.mock import patch, MagicMock
from src.services.gebruikercreate import GebruikerService
from src.services.gebruikercreate_exceptions import (
    GebruikerAlreadyExistsException,
    InvalidGebruikerDataException,
    StorageException
)

def setup_function():
    # Reset in-memory db tussen tests
    from src.services import gebruikercreate
    gebruikercreate.ingebouwde_db.clear()

def test_create_gebruiker_success():
    gebruiker_data = {"naam": "Jan", "email": "jan@example.com"}
    service = GebruikerService()
    result = service.create(gebruiker_data)
    assert result["naam"] == "Jan"
    assert result["email"] == "jan@example.com"
    assert "id" in result

def test_create_gebruiker_already_exists():
    gebruiker_data = {"naam": "Piet", "email": "piet@example.com"}
    service = GebruikerService()
    service.create(gebruiker_data)
    with pytest.raises(GebruikerAlreadyExistsException):
        service.create(gebruiker_data)

def test_create_gebruiker_invalid_data():
    gebruiker_data = {"naam": "", "email": "geenemail"}
    service = GebruikerService()
    with pytest.raises(InvalidGebruikerDataException):
        service.create(gebruiker_data)

def test_create_gebruiker_storage_exception():
    gebruiker_data = {"naam": "Joris", "email": "joris@example.com"}
    service = GebruikerService()
    # Forceer een exception door ingebouwde_db onbeschikbaar te maken
    with patch("src.services.gebruikercreate.ingebouwde_db", None):
        with pytest.raises(StorageException):
            service.create(gebruiker_data)
