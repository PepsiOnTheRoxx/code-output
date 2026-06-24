import pytest

class BronService:
    def __init__(self):
        self.bronnen = []

    def create_bron(self, element_type, element_id):
        if not isinstance(element_type, str) or not isinstance(element_id, int):
            raise ValueError("Invalid input types.")
        bron = {"ElementType": element_type, "ElementID": element_id}
        self.bronnen.append(bron)
        return bron

    def get_bronnen(self):
        return self.bronnen


def test_create_bron_with_valid_data():
    service = BronService()
    bron = service.create_bron("ObjectType", 12)
    assert bron == {"ElementType": "ObjectType", "ElementID": 12}
    assert service.get_bronnen() == [bron]


def test_create_bron_with_another_valid_data():
    service = BronService()
    bron = service.create_bron("Attribute", 15)
    assert bron == {"ElementType": "Attribute", "ElementID": 15}
    assert service.get_bronnen() == [bron]


def test_create_multiple_brons():
    service = BronService()
    service.create_bron("ObjectType", 12)
    service.create_bron("Attribute", 15)
    service.create_bron("Attribute", 16)

    assert service.get_bronnen() == [
        {"ElementType": "ObjectType", "ElementID": 12},
        {"ElementType": "Attribute", "ElementID": 15},
        {"ElementType": "Attribute", "ElementID": 16}
    ]


def test_create_bron_with_invalid_element_type():
    service = BronService()
    with pytest.raises(ValueError):
        service.create_bron(123, 12)


def test_create_bron_with_invalid_element_id():
    service = BronService()
    with pytest.raises(ValueError):
        service.create_bron("ObjectType", "12")