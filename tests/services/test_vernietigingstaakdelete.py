import pytest
from unittest.mock import patch, MagicMock
from src.services.vernietigingstaakdelete import VernietigingstaakService, SimpleDatastore
from src.services.vernietigingstaakdelete_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException,
)

@pytest.fixture
def service():
    # Gebruik een verse datastore per test
    return VernietigingstaakService(datastore=SimpleDatastore())

def test_delete_vernietigingstaak_success(service):
    service._datastore.add(123, MagicMock(id=123))
    service.delete_vernietigingstaak(123)
    assert 123 not in service._datastore.data

def test_delete_vernietigingstaak_not_found(service):
    with pytest.raises(VernietigingstaakNotFoundException):
        service.delete_vernietigingstaak(999)

def test_delete_vernietigingstaak_delete_exception(service):
    # Subclass om delete_by_id te laten falen
    class BrokenService(VernietigingstaakService):
        def delete_by_id(self, taak_id):
            raise VernietigingstaakDeleteException()
    broken_service = BrokenService(datastore=service._datastore)
    broken_service._datastore.add(1, MagicMock(id=1))
    with pytest.raises(VernietigingstaakDeleteException):
        broken_service.delete_vernietigingstaak(1)

def test_delete_vernietigingstaak_correct_id_passed_to_methods(service):
    with patch.object(service, "get_by_id", return_value=MagicMock(id=321)) as mock_get, \
         patch.object(service, "delete_by_id", return_value=None) as mock_delete:
        service.delete_vernietigingstaak(321)
        mock_get.assert_called_once_with(321)
        mock_delete.assert_called_once_with(321)
