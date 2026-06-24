import pytest
from src.bronservice import BronService, Bron

@pytest.fixture
def bron_data():
    return {
        "name": "BronX",
        "type": "Water",
        "attributes": {
            "Attribute15": "Waarde15",
            "Attribute16": "Waarde16"
        }
    }

def test_create_bron_returns_bron_object(bron_data):
    service = BronService()
    bron = service.create_bron(**bron_data)
    assert isinstance(bron, Bron)
    assert bron.name == bron_data["name"]
    assert bron.type == bron_data["type"]
    assert bron.attributes["Attribute15"] == "Waarde15"
    assert bron.attributes["Attribute16"] == "Waarde16"

def test_create_bron_assigns_all_attributes(bron_data):
    service = BronService()
    bron = service.create_bron(**bron_data)
    assert len(bron.attributes) == 2
    assert set(bron.attributes.keys()) == {"Attribute15", "Attribute16"}

def test_create_bron_with_missing_attribute_raises(bron_data):
    service = BronService()
    invalid_data = bron_data.copy()
    invalid_data["attributes"] = {"Attribute15": "Waarde15"}  # Missing Attribute16
    with pytest.raises(ValueError):
        service.create_bron(**invalid_data)

def test_create_bron_with_invalid_element_id_raises():
    service = BronService()
    bron_data = {
        "name": "BronY",
        "type": "Water",
        "attributes": {
            "Attribute999": "Waarde999",
            "Attribute15": "Waarde15"
        }
    }
    with pytest.raises(KeyError):
        service.create_bron(**bron_data)

def test_create_bron_persists_bron(bron_data):
    service = BronService()
    bron = service.create_bron(**bron_data)
    # Assuming service has internal list of brons
    assert bron in service.get_all_brons()