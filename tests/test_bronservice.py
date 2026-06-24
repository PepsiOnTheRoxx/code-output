import pytest
from src.bronservice import BronService, Bron

@pytest.fixture
def bron_service():
    return BronService()

def test_create_bron_success(bron_service):
    data = {
        "name": "Test Bron",
        "element_type": [{"ElementType": "ObjectType", "ElementID": 12}],
        "attributes": [{"ElementType": "Attribute", "ElementID": 15}, {"ElementType": "Attribute", "ElementID": 16}]
    }
    bron = bron_service.create_bron(data)
    assert bron.name == "Test Bron"
    assert bron.element_type == [{"ElementType": "ObjectType", "ElementID": 12}]
    assert bron.attributes == [{"ElementType": "Attribute", "ElementID": 15}, {"ElementType": "Attribute", "ElementID": 16}]

def test_create_bron_missing_name(bron_service):
    data = {
        "element_type": [{"ElementType": "ObjectType", "ElementID": 12}],
        "attributes": [{"ElementType": "Attribute", "ElementID": 15}, {"ElementType": "Attribute", "ElementID": 16}]
    }
    with pytest.raises(ValueError, match="Name is required"):
        bron_service.create_bron(data)

def test_create_bron_invalid_element_type(bron_service):
    data = {
        "name": "Test Bron",
        "element_type": [{"ElementType": "InvalidType", "ElementID": 99}],
        "attributes": [{"ElementType": "Attribute", "ElementID": 15}, {"ElementType": "Attribute", "ElementID": 16}]
    }
    with pytest.raises(ValueError, match="Invalid element type"):
        bron_service.create_bron(data)

def test_create_bron_no_attributes(bron_service):
    data = {
        "name": "Test Bron",
        "element_type": [{"ElementType": "ObjectType", "ElementID": 12}],
        "attributes": []
    }
    bron = bron_service.create_bron(data)
    assert bron.attributes == []

def test_create_bron_duplicate_element_id(bron_service):
    data = {
        "name": "Test Bron",
        "element_type": [{"ElementType": "ObjectType", "ElementID": 12}, {"ElementType": "ObjectType", "ElementID": 12}],
        "attributes": [{"ElementType": "Attribute", "ElementID": 15}, {"ElementType": "Attribute", "ElementID": 16}]
    }
    with pytest.raises(ValueError, match="Duplicate ElementID found"):
        bron_service.create_bron(data)