import pytest
from unittest.mock import patch, MagicMock
from src.services.deletebron import DeleteBron, BronService
from src.services.deletebron_exceptions import BronNotFoundException, DeleteBronException

class SimpleBron:
    def __init__(self, id):
        self.id = id

def test_deletebron_success():
    bron_service = BronService()
    bron_id = 123
    bron_obj = SimpleBron(bron_id)
    bron_service.add_bron(bron_obj)

    DeleteBron(bron_service).execute(bron_id)
    assert bron_service.get_bron_by_id(bron_id) is None

def test_deletebron_bron_not_found():
    bron_service = BronService()
    bron_id = 999
    with pytest.raises(BronNotFoundException):
        DeleteBron(bron_service).execute(bron_id)

def test_deletebron_delete_exception():
    bron_service = BronService()
    bron_id = 321
    bron_obj = SimpleBron(bron_id)
    bron_service.add_bron(bron_obj)

    # Patch delete_bron to raise DeleteBronException
    with patch.object(bron_service, 'delete_bron', side_effect=DeleteBronException):
        with pytest.raises(DeleteBronException):
            DeleteBron(bron_service).execute(bron_id)
