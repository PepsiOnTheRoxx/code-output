import pytest
from src.services.createvernietigingstaak import VernietigingstaakService
from src.services.createvernietigingstaak_exceptions import (
    DuplicateVernietigingstaakException,
    InvalidVernietigingstaakDataException,
    MissingVernietigingstaakAttributeException
)


@pytest.fixture
def vernietigingstaak_service():
    return VernietigingstaakService()


def test_create_vernietigingstaak_success(vernietigingstaak_service):
    data = {
        "objecttype_id": 10,
        "attribute_10": "some value",
        "attribute_11": 123,
        "attribute_12": True
    }
    result = vernietigingstaak_service.create_vernietigingstaak(data)
    assert result is not None
    assert result.objecttype_id == 10
    assert result.attribute_10 == "some value"
    assert result.attribute_11 == 123
    assert result.attribute_12 is True


def test_create_vernietigingstaak_missing_required_attribute(vernietigingstaak_service):
    data = {
        "objecttype_id": 10,
        "attribute_10": "some value",
        "attribute_11": 123
        # attribute_12 ontbreekt
    }
    with pytest.raises(MissingVernietigingstaakAttributeException):
        vernietigingstaak_service.create_vernietigingstaak(data)


def test_create_vernietigingstaak_invalid_data(vernietigingstaak_service):
    data = {
        "objecttype_id": 10,
        "attribute_10": "some value",
        "attribute_11": "ongeldige waarde",
        "attribute_12": True
    }
    with pytest.raises(InvalidVernietigingstaakDataException):
        vernietigingstaak_service.create_vernietigingstaak(data)


def test_create_vernietigingstaak_duplicate(vernietigingstaak_service):
    data = {
        "objecttype_id": 10,
        "attribute_10": "unique value",
        "attribute_11": 456,
        "attribute_12": False
    }
    vernietigingstaak_service.create_vernietigingstaak(data)
    with pytest.raises(DuplicateVernietigingstaakException):
        vernietigingstaak_service.create_vernietigingstaak(data)
