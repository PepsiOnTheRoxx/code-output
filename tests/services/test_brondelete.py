import pytest
from src.services.brondelete import BronService
from src.services.brondelete_exceptions import BronNotFoundException, BronDeleteException
from unittest.mock import MagicMock

@pytest.fixture
def bron_service():
    service = BronService()
    service.bron_exists = MagicMock()
    service.delete_bron = MagicMock()
    return service

def test_delete_existing_bron(bron_service):
    bron_id = 1
    bron_service.bron_exists.return_value = True
    bron_service.delete_bron.return_value = None

    bron_service.delete(bron_id)

    bron_service.bron_exists.assert_called_once_with(bron_id)
    bron_service.delete_bron.assert_called_once_with(bron_id)

def test_delete_non_existing_bron_raises(bron_service):
    bron_id = 999
    bron_service.bron_exists.return_value = False

    with pytest.raises(BronNotFoundException):
        bron_service.delete(bron_id)

    bron_service.bron_exists.assert_called_once_with(bron_id)
    bron_service.delete_bron.assert_not_called()

def test_delete_bron_fails_raises(bron_service):
    bron_id = 2
    bron_service.bron_exists.return_value = True
    bron_service.delete_bron.side_effect = BronDeleteException("Delete failed")

    with pytest.raises(BronDeleteException):
        bron_service.delete(bron_id)

    bron_service.bron_exists.assert_called_once_with(bron_id)
    bron_service.delete_bron.assert_called_once_with(bron_id)

def test_delete_calls_in_order(bron_service):
    bron_id = 3
    bron_service.bron_exists.return_value = True
    bron_service.delete_bron.return_value = None

    bron_service.delete(bron_id)

    assert bron_service.bron_exists.call_count == 1
    assert bron_service.delete_bron.call_count == 1
    assert bron_service.bron_exists.call_args_list[0][0][0] == bron_id
    assert bron_service.delete_bron.call_args_list[0][0][0] == bron_id
