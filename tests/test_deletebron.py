import pytest
from src.deletebron import BronService, BronNotFoundException

@pytest.fixture
def bron_service():
    return BronService()

def test_delete_existing_bron(bron_service):
    bron_id = bron_service.create_bron(name="Bron 1")
    assert bron_service.get_bron(bron_id) is not None
    bron_service.delete_bron(bron_id)
    with pytest.raises(BronNotFoundException):
        bron_service.get_bron(bron_id)

def test_delete_non_existing_bron_raises(bron_service):
    invalid_bron_id = 999
    with pytest.raises(BronNotFoundException):
        bron_service.delete_bron(invalid_bron_id)

def test_delete_bron_twice_raises_exception(bron_service):
    bron_id = bron_service.create_bron(name="Bron 2")
    bron_service.delete_bron(bron_id)
    with pytest.raises(BronNotFoundException):
        bron_service.delete_bron(bron_id)

def test_delete_other_bron_remains_untouched(bron_service):
    bron_id1 = bron_service.create_bron(name="Bron 1")
    bron_id2 = bron_service.create_bron(name="Bron 2")
    bron_service.delete_bron(bron_id1)
    assert bron_service.get_bron(bron_id2) is not None

def test_delete_bron_returns_none(bron_service):
    bron_id = bron_service.create_bron(name="Bron 3")
    result = bron_service.delete_bron(bron_id)
    assert result is None