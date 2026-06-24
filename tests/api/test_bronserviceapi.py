import pytest
from unittest.mock import patch
from src.api import bronserviceapi
from src.api.bronserviceapi_exceptions import BronAPINotFoundException, BronAPIValidationException

def test_get_bron_success():
    with patch('src.api.bronserviceapi.get_bron_by_id') as mock_get:
        mock_get.return_value = {"id": 1, "naam": "TestBron"}
        result = bronserviceapi.get_bron_by_id(1)
        assert result == {"id": 1, "naam": "TestBron"}
        mock_get.assert_called_once_with(1)

def test_get_bron_not_found():
    with patch('src.api.bronserviceapi.get_bron_by_id') as mock_get:
        mock_get.side_effect = BronAPINotFoundException("Bron not found")
        with pytest.raises(BronAPINotFoundException) as excinfo:
            bronserviceapi.get_bron_by_id(99)
        assert "Bron not found" in str(excinfo.value)
        mock_get.assert_called_once_with(99)

def test_create_bron_success():
    with patch('src.api.bronserviceapi.create_bron') as mock_create:
        input_data = {"naam": "NieuweBron"}
        mock_create.return_value = {"id": 2, "naam": "NieuweBron"}
        result = bronserviceapi.create_bron(input_data)
        assert result == {"id": 2, "naam": "NieuweBron"}
        mock_create.assert_called_once_with(input_data)

def test_create_bron_validation_error():
    with patch('src.api.bronserviceapi.create_bron') as mock_create:
        invalid_data = {"naam": ""}
        mock_create.side_effect = BronAPIValidationException("Naam mag niet leeg zijn")
        with pytest.raises(BronAPIValidationException) as excinfo:
            bronserviceapi.create_bron(invalid_data)
        assert "Naam mag niet leeg zijn" in str(excinfo.value)
        mock_create.assert_called_once_with(invalid_data)

def test_update_bron_success():
    with patch('src.api.bronserviceapi.update_bron') as mock_update:
        bron_id = 1
        update_data = {"naam": "BijgewerktBron"}
        mock_update.return_value = {"id": bron_id, "naam": "BijgewerktBron"}
        result = bronserviceapi.update_bron(bron_id, update_data)
        assert result == {"id": bron_id, "naam": "BijgewerktBron"}
        mock_update.assert_called_once_with(bron_id, update_data)

def test_update_bron_not_found():
    with patch('src.api.bronserviceapi.update_bron') as mock_update:
        bron_id = 99
        update_data = {"naam": "BijgewerktBron"}
        mock_update.side_effect = BronAPINotFoundException("Bron niet gevonden")
        with pytest.raises(BronAPINotFoundException) as excinfo:
            bronserviceapi.update_bron(bron_id, update_data)
        assert "Bron niet gevonden" in str(excinfo.value)
        mock_update.assert_called_once_with(bron_id, update_data)

def test_delete_bron_success():
    with patch('src.api.bronserviceapi.delete_bron') as mock_delete:
        mock_delete.return_value = True
        result = bronserviceapi.delete_bron(1)
        assert result is True
        mock_delete.assert_called_once_with(1)

def test_delete_bron_not_found():
    with patch('src.api.bronserviceapi.delete_bron') as mock_delete:
        mock_delete.side_effect = BronAPINotFoundException("Bron niet gevonden")
        with pytest.raises(BronAPINotFoundException):
            bronserviceapi.delete_bron(99)
        mock_delete.assert_called_once_with(99)

def test_list_bronnen_success():
    with patch('src.api.bronserviceapi.list_bronnen') as mock_list:
        mock_list.return_value = [
            {"id": 1, "naam": "Bron1"},
            {"id": 2, "naam": "Bron2"}
        ]
        result = bronserviceapi.list_bronnen()
        assert isinstance(result, list)
        assert len(result) == 2
        mock_list.assert_called_once_with()
