import pytest
from src.services.readbron import BronService
from src.services.readbron_exceptions import BronNotFoundException, InvalidBronIDException

@pytest.fixture
def bron_service():
    return BronService()

def test_read_bron_existing_id(bron_service):
    bron_id = 1
    bron = bron_service.read_bron(bron_id)
    assert bron is not None
    assert isinstance(bron, dict)
    assert bron.get("ElementType") == "ObjectType"
    assert bron.get("ElementID") == 12

def test_read_bron_non_existing_id_raises(bron_service):
    non_existing_id = 9999
    with pytest.raises(BronNotFoundException):
        bron_service.read_bron(non_existing_id)

def test_read_bron_invalid_id_raises(bron_service):
    invalid_id = "invalid"
    with pytest.raises(InvalidBronIDException):
        bron_service.read_bron(invalid_id)

def test_read_bron_none_id_raises(bron_service):
    with pytest.raises(InvalidBronIDException):
        bron_service.read_bron(None)

def test_read_bron_returns_expected_fields(bron_service):
    bron_id = 1
    bron = bron_service.read_bron(bron_id)
    assert "ElementType" in bron
    assert "ElementID" in bron
    assert bron["ElementType"] == "ObjectType"
    assert bron["ElementID"] == 12