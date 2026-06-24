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
    taak_data = {"attribute_10": "waarde1", "attribute_11": "waarde2", "attribute_12": "waarde3"}
    with patch.object(service, "_exists", return_value=False), \
         patch.object(service, "_save", return_value=42) as mock_save:
        taak_id = service.create_vernietigingstaak(taak_data)
        assert taak_id == 42
        mock_save.assert_called_once_with(taak_data)

def test_create_vernietigingstaak_already_exists():
    service = VernietigingstaakService()
    taak_data = {"attribute_10": "waarde1", "attribute_11": "waarde2", "attribute_12": "waarde3"}
    with patch.object(service, "_exists", return_value=True):
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
    taak_data = {"attribute_10": "waarde1", "attribute_11": "waarde2", "attribute_12": "waarde3"}
    with patch.object(service, "_exists", return_value=False), \
         patch.object(service, "_save", side_effect=DatabaseException("DB error")):
        with pytest.raises(DatabaseException) as exc_info:
            service.create_vernietigingstaak(taak_data)
        assert "DB error" in str(exc_info.value)