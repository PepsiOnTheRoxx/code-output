import pytest
from unittest.mock import patch, MagicMock
from src.api.vernietigingstaakserviceapi import VernietigingstaakAPI
from src.api.vernietigingstaakserviceapi_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakValidationException,
    VernietigingstaakConflictException
)

@pytest.fixture
def api():
    return VernietigingstaakAPI()

def test_create_vernietigingstaak_success(api):
    vernietigingstaak_data = {"naam": "Test Taak"}
    created = {"id": 1, "naam": "Test Taak"}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.create", return_value=created) as mock_create:
        result = api.create_vernietigingstaak(vernietigingstaak_data)
        mock_create.assert_called_once_with(vernietigingstaak_data)
        assert result == created

def test_create_vernietigingstaak_validation_error(api):
    vernietigingstaak_data = {"naam": ""}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.create", side_effect=VernietigingstaakValidationException("Invalid")):
        with pytest.raises(VernietigingstaakValidationException):
            api.create_vernietigingstaak(vernietigingstaak_data)

def test_get_vernietigingstaak_success(api):
    taak_id = 1
    taak_data = {"id": 1, "naam": "Taak A"}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.get", return_value=taak_data) as mock_get:
        result = api.get_vernietigingstaak(taak_id)
        mock_get.assert_called_once_with(taak_id)
        assert result == taak_data

def test_get_vernietigingstaak_not_found(api):
    taak_id = 42
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.get", side_effect=VernietigingstaakNotFoundException("Not found")):
        with pytest.raises(VernietigingstaakNotFoundException):
            api.get_vernietigingstaak(taak_id)

def test_update_vernietigingstaak_success(api):
    taak_id = 2
    update_data = {"naam": "Nieuwe Naam"}
    updated = {"id": 2, "naam": "Nieuwe Naam"}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.update", return_value=updated) as mock_update:
        result = api.update_vernietigingstaak(taak_id, update_data)
        mock_update.assert_called_once_with(taak_id, update_data)
        assert result == updated

def test_update_vernietigingstaak_validation_error(api):
    taak_id = 2
    update_data = {"naam": ""}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.update", side_effect=VernietigingstaakValidationException("Invalid data")):
        with pytest.raises(VernietigingstaakValidationException):
            api.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_not_found(api):
    taak_id = 123
    update_data = {"naam": "Onbekende Taak"}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.update", side_effect=VernietigingstaakNotFoundException("Not found")):
        with pytest.raises(VernietigingstaakNotFoundException):
            api.update_vernietigingstaak(taak_id, update_data)

def test_delete_vernietigingstaak_success(api):
    taak_id = 4
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.delete", return_value=None) as mock_delete:
        assert api.delete_vernietigingstaak(taak_id) is None
        mock_delete.assert_called_once_with(taak_id)

def test_delete_vernietigingstaak_not_found(api):
    taak_id = 777
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.delete", side_effect=VernietigingstaakNotFoundException("Missing")):
        with pytest.raises(VernietigingstaakNotFoundException):
            api.delete_vernietigingstaak(taak_id)

def test_create_vernietigingstaak_conflict(api):
    vernietigingstaak_data = {"naam": "Duplicaat"}
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.create", side_effect=VernietigingstaakConflictException("Conflict")):
        with pytest.raises(VernietigingstaakConflictException):
            api.create_vernietigingstaak(vernietigingstaak_data)

def test_list_vernietigingstaken(api):
    expected = [
        {"id": 1, "naam": "A"},
        {"id": 2, "naam": "B"}
    ]
    with patch("src.api.vernietigingstaakserviceapi.VernietigingstaakService.list", return_value=expected) as mock_list:
        result = api.list_vernietigingstaken()
        mock_list.assert_called_once_with()
        assert result == expected
