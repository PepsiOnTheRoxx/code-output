import pytest
from unittest.mock import patch, MagicMock
from src.services.vernietigingstaakdelete import VernietigingstaakService
from src.services.vernietigingstaakdelete_exceptions import VernietigingstaakNotFoundException, VernietigingstaakDeleteException

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_delete_vernietigingstaak_success(service):
    with patch.object(service, "get_by_id", return_value=MagicMock(id=123)) as mock_get, \
         patch.object(service, "delete_by_id", return_value=None) as mock_delete:
        service.delete_vernietigingstaak(123)
        mock_get.assert_called_once_with(123)
        mock_delete.assert_called_once_with(123)

def test_delete_vernietigingstaak_not_found(service):
    with patch.object(service, "get_by_id", side_effect=VernietigingstaakNotFoundException()):
        with pytest.raises(VernietigingstaakNotFoundException):
            service.delete_vernietigingstaak(999)

def test_delete_vernietigingstaak_delete_exception(service):
    with patch.object(service, "get_by_id", return_value=MagicMock(id=1)), \
         patch.object(service, "delete_by_id", side_effect=VernietigingstaakDeleteException()):
        with pytest.raises(VernietigingstaakDeleteException):
            service.delete_vernietigingstaak(1)

def test_delete_vernietigingstaak_correct_id_passed_to_methods(service):
    with patch.object(service, "get_by_id", return_value=MagicMock(id=321)) as mock_get, \
         patch.object(service, "delete_by_id", return_value=None) as mock_delete:
        service.delete_vernietigingstaak(321)
        mock_get.assert_called_once_with(321)
        mock_delete.assert_called_once_with(321)