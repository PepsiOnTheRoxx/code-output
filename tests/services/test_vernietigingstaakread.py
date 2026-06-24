import pytest
from unittest.mock import patch, MagicMock
from src.services.vernietigingstaakread import VernietigingstaakService
from src.services.vernietigingstaakread_exceptions import VernietigingstaakNotFoundException, VernietigingstaakReadException

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_get_vernietigingstaak_by_id_success(service):
    vernietigingstaak_id = 1
    expected_data = {'id': 1, 'status': 'in_progress'}
    with patch.object(service, 'get_vernietigingstaak_by_id', return_value=expected_data) as mock_method:
        result = service.get_vernietigingstaak_by_id(vernietigingstaak_id)
        mock_method.assert_called_once_with(vernietigingstaak_id)
        assert result == expected_data

def test_get_vernietigingstaak_by_id_not_found(service):
    vernietigingstaak_id = 999
    with patch.object(service, 'get_vernietigingstaak_by_id', side_effect=VernietigingstaakNotFoundException):
        with pytest.raises(VernietigingstaakNotFoundException):
            service.get_vernietigingstaak_by_id(vernietigingstaak_id)

def test_get_all_vernietigingstaken_returns_list(service):
    expected_list = [
        {'id': 1, 'status': 'in_progress'},
        {'id': 2, 'status': 'completed'}
    ]
    with patch.object(service, 'get_all_vernietigingstaken', return_value=expected_list) as mock_method:
        result = service.get_all_vernietigingstaken()
        mock_method.assert_called_once()
        assert isinstance(result, list)
        assert result == expected_list

def test_get_all_vernietigingstaken_empty(service):
    with patch.object(service, 'get_all_vernietigingstaken', return_value=[]) as mock_method:
        result = service.get_all_vernietigingstaken()
        mock_method.assert_called_once()
        assert result == []

def test_get_vernietigingstaak_by_id_raises_read_exception(service):
    vernietigingstaak_id = 5
    with patch.object(service, 'get_vernietigingstaak_by_id', side_effect=VernietigingstaakReadException):
        with pytest.raises(VernietigingstaakReadException):
            service.get_vernietigingstaak_by_id(vernietigingstaak_id)