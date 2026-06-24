import pytest
from unittest.mock import patch, MagicMock
from src.services.deletebron import DeleteBron, BronService
from src.services.deletebron_exceptions import BronNotFoundException, DeleteBronException

def test_deletebron_success():
    bron_service = BronService()
    bron_id = 123

    with patch.object(bron_service, 'get_bron_by_id', return_value=MagicMock(id=bron_id)):
        with patch.object(bron_service, 'delete_bron') as mock_delete:
            mock_delete.return_value = None
            DeleteBron(bron_service).execute(bron_id)
            mock_delete.assert_called_once_with(bron_id)

def test_deletebron_bron_not_found():
    bron_service = BronService()
    bron_id = 999

    with patch.object(bron_service, 'get_bron_by_id', return_value=None):
        with pytest.raises(BronNotFoundException):
            DeleteBron(bron_service).execute(bron_id)

def test_deletebron_delete_exception():
    bron_service = BronService()
    bron_id = 321
    bron_obj = MagicMock(id=bron_id)

    with patch.object(bron_service, 'get_bron_by_id', return_value=bron_obj):
        with patch.object(bron_service, 'delete_bron', side_effect=DeleteBronException):
            with pytest.raises(DeleteBronException):
                DeleteBron(bron_service).execute(bron_id)
