import pytest
from unittest.mock import patch, MagicMock
from src.services.vernietigingstaakcreate import VernietigingstaakService
from src.services.vernietigingstaakcreate_exceptions import (
    VernietigingstaakAlreadyExistsException,
    InvalidVernietigingstaakDataException,
    DatabaseException
)

def test_create_vernietigingstaak_success():
    service = VernietigingstaakService()
    # reset store voor isolation
    from src.services.vernietigingstaakcreate import _vernietigingstaak_store
    _vernietigingstaak_store.clear()
    taak_data = {"attribute_10": "waarde1", "attribute_11": "waarde2", "attribute_12": "waarde3"}
    taak_id = service.create_vernietigingstaak(taak_data)
    assert taak_id == 1
    assert len(_vernietigingstaak_store) == 1
    assert _vernietigingstaak_store[0]["attribute_10"] == "waarde1"


def test_create_vernietigingstaak_already_exists():
    service = VernietigingstaakService()
    from src.services.vernietigingstaakcreate import _vernietigingstaak_store
    _vernietigingstaak_store.clear()
    taak_data = {"attribute_10": "waarde1", "attribute_11": "waarde2", "attribute_12": "waarde3"}
    # Eerst een keer aanmaken
    service.create_vernietigingstaak(taak_data)
    # Daarnazelfde data opnieuw -> exceptie
    with pytest.raises(VernietigingstaakAlreadyExistsException):
        service.create_vernietigingstaak(taak_data)


def test_create_vernietigingstaak_invalid_data_missing_attribute():
    service = VernietigingstaakService()
    taak_data = {"attribute_10": "waarde1", "attribute_12": "waarde3"}  # attribute_11 ontbreekt
    with pytest.raises(InvalidVernietigingstaakDataException):
        service.create_vernietigingstaak(taak_data)


def test_create_vernietigingstaak_invalid_data_none():
    service = VernietigingstaakService()
    taak_data = None
    with pytest.raises(InvalidVernietigingstaakDataException):
        service.create_vernietigingstaak(taak_data)


def test_create_vernietigingstaak_fails_on_db_error():
    service = VernietigingstaakService()
    from src.services.vernietigingstaakcreate import _vernietigingstaak_store
    _vernietigingstaak_store.clear()
    taak_data = {"attribute_10": "waarde1", "attribute_11": "waarde2", "attribute_12": "waarde3", "force_db_error": True}
    with pytest.raises(DatabaseException) as exc_info:
        service.create_vernietigingstaak(taak_data)
    assert "DB error" in str(exc_info.value)
