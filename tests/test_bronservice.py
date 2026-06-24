import pytest

class BronNotFoundException(Exception):
    pass

class BronService:
    def __init__(self):
        self.bronnen = {
            12: {"naam": "Basis Bron", "type": "Watertype", "locatie": "Nederland"}
        }

    def read_bron(self, element_id):
        if element_id not in self.bronnen:
            raise BronNotFoundException(f"Bron met ID {element_id} niet gevonden.")
        return self.bronnen[element_id]

def test_read_existing_bron():
    service = BronService()
    bron = service.read_bron(12)
    assert bron == {"naam": "Basis Bron", "type": "Watertype", "locatie": "Nederland"}

def test_read_non_existing_bron():
    service = BronService()
    with pytest.raises(BronNotFoundException, match="Bron met ID 99 niet gevonden."):
        service.read_bron(99)

def test_read_bron_properties():
    service = BronService()
    bron = service.read_bron(12)
    assert "naam" in bron
    assert "type" in bron
    assert "locatie" in bron

def test_read_bron_locatie():
    service = BronService()
    bron = service.read_bron(12)
    assert bron["locatie"] == "Nederland"

def test_read_bron_type():
    service = BronService()
    bron = service.read_bron(12)
    assert bron["type"] == "Watertype"