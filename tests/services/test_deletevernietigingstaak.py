import pytest
from unittest.mock import patch, MagicMock
from src.services.deletevernietigingstaak import VernietigingstaakService, seed_vernietigingstaken, Vernietigingstaak
from src.services.deletevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException,
)

def test_delete_vernietigingstaak_succeeds():
    seed_vernietigingstaken([42])
    service = VernietigingstaakService()
    service.delete_vernietigingstaak(42)
    assert service.get_vernietigingstaak_by_id(42) is None

def test_delete_vernietigingstaak_not_found():
    seed_vernietigingstaken([])
    service = VernietigingstaakService()
    with pytest.raises(VernietigingstaakNotFoundException):
        service.delete_vernietigingstaak(99)

def test_delete_vernietigingstaak_delete_exception():
    service = VernietigingstaakService()
    mock_task = MagicMock()
    with patch.object(service, 'get_vernietigingstaak_by_id', return_value=mock_task), \
         patch.object(service, 'delete_vernietigingstaak_from_db', side_effect=VernietigingstaakDeleteException):
        with pytest.raises(VernietigingstaakDeleteException):
            service.delete_vernietigingstaak(99)

def test_delete_vernietigingstaak_calls_proper_methods():
    service = VernietigingstaakService()
    mock_task = MagicMock()
    with patch.object(service, 'get_vernietigingstaak_by_id', return_value=mock_task) as mock_get, \
         patch.object(service, 'delete_vernietigingstaak_from_db', return_value=None) as mock_delete:
        identificatie = 123
        service.delete_vernietigingstaak(identificatie)
        mock_get.assert_called_once_with(identificatie)
        mock_delete.assert_called_once_with(mock_task)

def test_delete_vernietigingstaak_propagates_unexpected_error():
    service = VernietigingstaakService()
    mock_task = MagicMock()
    with patch.object(service, 'get_vernietigingstaak_by_id', return_value=mock_task), \
         patch.object(service, 'delete_vernietigingstaak_from_db', side_effect=RuntimeError("DB Error")):
        with pytest.raises(RuntimeError):
            service.delete_vernietigingstaak(81)
