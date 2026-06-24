import pytest

class Bron:
    def __init__(self, element_type, element_id):
        self.element_type = element_type
        self.element_id = element_id

class BronService:
    def create_bron(self, element_type, element_id):
        if element_type not in ["ObjectType", "Attribute"]:
            raise ValueError("Invalid element type")
        if not isinstance(element_id, int) or element_id <= 0:
            raise ValueError("Element ID must be a positive integer")
        
        return Bron(element_type, element_id)

def test_create_bron_with_valid_object_type():
    service = BronService()
    bron = service.create_bron("ObjectType", 12)
    assert bron.element_type == "ObjectType"
    assert bron.element_id == 12

def test_create_bron_with_valid_attribute_type():
    service = BronService()
    bron = service.create_bron("Attribute", 15)
    assert bron.element_type == "Attribute"
    assert bron.element_id == 15

def test_create_bron_with_another_valid_attribute_type():
    service = BronService()
    bron = service.create_bron("Attribute", 16)
    assert bron.element_type == "Attribute"
    assert bron.element_id == 16

def test_create_bron_with_invalid_element_type():
    service = BronService()
    with pytest.raises(ValueError, match="Invalid element type"):
        service.create_bron("InvalidType", 12)

def test_create_bron_with_negative_element_id():
    service = BronService()
    with pytest.raises(ValueError, match="Element ID must be a positive integer"):
        service.create_bron("Attribute", -1)

def test_create_bron_with_zero_element_id():
    service = BronService()
    with pytest.raises(ValueError, match="Element ID must be a positive integer"):
        service.create_bron("ObjectType", 0)

def test_create_bron_with_non_integer_element_id():
    service = BronService()
    with pytest.raises(ValueError, match="Element ID must be a positive integer"):
        service.create_bron("ObjectType", "string")