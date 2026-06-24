import pytest
from src.services.createbron import BronService
from src.services.createbron_exceptions import BronAlreadyExistsException, InvalidBronDataException

@pytest.fixture
def bron_service():
    return BronService()

def test_create_bron_success(bron_service):
    bron_data = {
        "ElementType": "ObjectType",
        "ElementID": 12,
        "attributes": [
            {"AttributeID": 15, "value": "NaamBron"},
            {"AttributeID": 16, "value": "OmschrijvingBron"}
        ]
    }
    bron = bron_service.create_bron(bron_data)
    assert bron is not None
    assert bron.element_type == "ObjectType"
    assert bron.element_id == 12
    assert any(attr.attribute_id == 15 and attr.value == "NaamBron" for attr in bron.attributes)
    assert any(attr.attribute_id == 16 and attr.value == "OmschrijvingBron" for attr in bron.attributes)

def test_create_bron_already_exists(bron_service, monkeypatch):
    bron_data = {
        "ElementType": "ObjectType",
        "ElementID": 12,
        "attributes": [
            {"AttributeID": 15, "value": "NaamBron"},
            {"AttributeID": 16, "value": "OmschrijvingBron"}
        ]
    }
    monkeypatch.setattr(bron_service, 'bron_exists', lambda _: True)
    with pytest.raises(BronAlreadyExistsException):
        bron_service.create_bron(bron_data)

def test_create_bron_invalid_data_missing_fields(bron_service):
    bron_data = {
        "ElementType": "ObjectType"
        # ElementID missing
    }
    with pytest.raises(InvalidBronDataException):
        bron_service.create_bron(bron_data)

def test_create_bron_invalid_attribute_id(bron_service):
    bron_data = {
        "ElementType": "ObjectType",
        "ElementID": 12,
        "attributes": [
            {"AttributeID": 999, "value": "OnbekendAttribuut"}
        ]
    }
    with pytest.raises(InvalidBronDataException):
        bron_service.create_bron(bron_data)

def test_create_bron_empty_attributes(bron_service):
    bron_data = {
        "ElementType": "ObjectType",
        "ElementID": 12,
        "attributes": []
    }
    with pytest.raises(InvalidBronDataException):
        bron_service.create_bron(bron_data)
