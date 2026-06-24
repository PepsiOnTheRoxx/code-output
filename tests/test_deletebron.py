import pytest
from src.deletebron import BronService
from src.deletebron_exceptions import BronNotFoundException, BronInUseException
from unittest.mock import Mock

def test_delete_bron_succeeds():
    bron_id = 42
    bron_repo = Mock()
    bron_repo.get_by_id.return_value = {"id": bron_id, "name": "bronX"}
    bron_repo.is_in_use.return_value = False
    bron_repo.delete = Mock()

    service = BronService(bron_repo)
    service.delete_bron(bron_id)

    bron_repo.get_by_id.assert_called_once_with(bron_id)
    bron_repo.is_in_use.assert_called_once_with(bron_id)
    bron_repo.delete.assert_called_once_with(bron_id)

def test_delete_bron_nonexistent_raises():
    bron_id = 123
    bron_repo = Mock()
    bron_repo.get_by_id.return_value = None
    bron_repo.is_in_use.return_value = False
    bron_repo.delete = Mock()

    service = BronService(bron_repo)
    with pytest.raises(BronNotFoundException):
        service.delete_bron(bron_id)

    bron_repo.get_by_id.assert_called_once_with(bron_id)
    bron_repo.is_in_use.assert_not_called()
    bron_repo.delete.assert_not_called()

def test_delete_bron_in_use_raises():
    bron_id = 5
    bron_repo = Mock()
    bron_repo.get_by_id.return_value = {"id": bron_id, "name": "bronY"}
    bron_repo.is_in_use.return_value = True
    bron_repo.delete = Mock()

    service = BronService(bron_repo)
    with pytest.raises(BronInUseException):
        service.delete_bron(bron_id)

    bron_repo.get_by_id.assert_called_once_with(bron_id)
    bron_repo.is_in_use.assert_called_once_with(bron_id)
    bron_repo.delete.assert_not_called()
