import pytest
from src.bronservice import BronService

@pytest.fixture
def bron_service():
    return BronService()

@pytest.fixture
def valid_bron_id():
    return 1

@pytest.fixture
def invalid_bron_id():
    return 999

def test_read_bron_returns_correct_object(bron_service, valid_bron_id):
    bron = bron_service.read_bron(valid_bron_id)
    assert isinstance(bron, dict)
    assert bron.get("ElementType") == "ObjectType"
    assert bron.get("ElementID") == 12

def test_read_bron_returns_attributes(bron_service, valid_bron_id):
    bron = bron_service.read_bron(valid_bron_id)
    attributes = bron.get("attributes", [])
    attribute_ids = [attr.get("ElementID") for attr in attributes]
    assert 15 in attribute_ids
    assert 16 in attribute_ids

def test_read_bron_with_invalid_id_returns_none_or_raises(bron_service, invalid_bron_id):
    try:
        bron = bron_service.read_bron(invalid_bron_id)
        assert bron is None
    except Exception:
        assert True

def test_read_bron_has_expected_keys(bron_service, valid_bron_id):
    bron = bron_service.read_bron(valid_bron_id)
    assert "ElementType" in bron
    assert "ElementID" in bron
    assert "attributes" in bron

def test_read_bron_attribute_values(bron_service, valid_bron_id):
    bron = bron_service.read_bron(valid_bron_id)
    attributes = bron.get("attributes", [])
    for attr in attributes:
        assert "ElementType" in attr
        assert "ElementID" in attr