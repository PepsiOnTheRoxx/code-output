import pytest
from unittest.mock import patch
from src.services.readvernietigingstaak import VernietigingstaakService
from src.services.readvernietigingstaak_exceptions import VernietigingstaakNotFoundException, VernietigingstaakInvalidInputException

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_read_vernietigingstaak_success(service):
    mock_taak = {"id": 10, "status": "GEPLAND"}
    with patch.object(service, 'get_by_id', return_value=mock_taak) as mock_get:
        result = service.read_vernietigingstaak(10)
        assert result == mock_taak
        mock_get.assert_called_once_with(10)

def test_read_vernietigingstaak_not_found(service):
    with patch.object(service, 'get_by_id', side_effect=VernietigingstaakNotFoundException("Not found")):
        with pytest.raises(VernietigingstaakNotFoundException):
            service.read_vernietigingstaak(99)

def test_read_vernietigingstaak_invalid_id(service):
    with patch.object(service, 'get_by_id', side_effect=VernietigingstaakInvalidInputException("Invalid ID")):
        with pytest.raises(VernietigingstaakInvalidInputException):
            service.read_vernietigingstaak("invalid")

def test_read_vernietigingstaak_calls_correct_method(service):
    with patch.object(service, 'get_by_id', return_value={}) as mock_get:
        service.read_vernietigingstaak(123)
        mock_get.assert_called_once_with(123)
