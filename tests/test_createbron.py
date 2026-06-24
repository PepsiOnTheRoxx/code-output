import pytest

class BronService:
    def __init__(self):
        self.bronnen = {}

    def create_bron(self, bron_id, attributes):
        if bron_id in self.bronnen:
            raise ValueError("Bron with this ID already exists.")
        self.bronnen[bron_id] = attributes

    def get_bron(self, bron_id):
        return self.bronnen.get(bron_id)

    def update_bron(self, bron_id, attributes):
        if bron_id not in self.bronnen:
            raise ValueError("Bron not found.")
        self.bronnen[bron_id] = attributes

    def delete_bron(self, bron_id):
        if bron_id not in self.bronnen:
            raise ValueError("Bron not found.")
        del self.bronnen[bron_id]


@pytest.fixture
def bron_service():
    return BronService()


def test_create_bron(bron_service):
    bron_id = 1
    attributes = [{"ElementType": "ObjectType", "ElementID": 12}]
    bron_service.create_bron(bron_id, attributes)
    assert bron_service.get_bron(bron_id) == attributes


def test_create_bron_duplicate_id(bron_service):
    bron_id = 2
    attributes = [{"ElementType": "Attribute", "ElementID": 15}]
    bron_service.create_bron(bron_id, attributes)
    with pytest.raises(ValueError, match="Bron with this ID already exists."):
        bron_service.create_bron(bron_id, attributes)


def test_update_bron(bron_service):
    bron_id = 3
    attributes = [{"ElementType": "Attribute", "ElementID": 16}]
    bron_service.create_bron(bron_id, attributes)
    new_attributes = [{"ElementType": "ObjectType", "ElementID": 12}]
    bron_service.update_bron(bron_id, new_attributes)
    assert bron_service.get_bron(bron_id) == new_attributes


def test_update_bron_not_found(bron_service):
    bron_id = 4
    new_attributes = [{"ElementType": "ObjectType", "ElementID": 12}]
    with pytest.raises(ValueError, match="Bron not found."):
        bron_service.update_bron(bron_id, new_attributes)


def test_delete_bron(bron_service):
    bron_id = 5
    attributes = [{"ElementType": "ObjectType", "ElementID": 12}]
    bron_service.create_bron(bron_id, attributes)
    bron_service.delete_bron(bron_id)
    assert bron_service.get_bron(bron_id) is None


def test_delete_bron_not_found(bron_service):
    bron_id = 6
    with pytest.raises(ValueError, match="Bron not found."):
        bron_service.delete_bron(bron_id)