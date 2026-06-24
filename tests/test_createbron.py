import pytest

class Bron:
    def __init__(self, naam, beschrijving):
        self.naam = naam
        self.beschrijving = beschrijving

class BronService:
    def create_bron(self, naam, beschrijving):
        if not naam or not beschrijving:
            raise ValueError("Naam en beschrijving zijn vereist.")
        return Bron(naam, beschrijving)

def test_create_bron_success():
    service = BronService()
    bron = service.create_bron("Test Bron", "Dit is een test bron.")
    assert bron.naam == "Test Bron"
    assert bron.beschrijving == "Dit is een test bron."

def test_create_bron_empty_naam():
    service = BronService()
    with pytest.raises(ValueError) as exc_info:
        service.create_bron("", "Dit is een test bron.")
    assert str(exc_info.value) == "Naam en beschrijving zijn vereist."

def test_create_bron_empty_beschrijving():
    service = BronService()
    with pytest.raises(ValueError) as exc_info:
        service.create_bron("Test Bron", "")
    assert str(exc_info.value) == "Naam en beschrijving zijn vereist."

def test_create_bron_empty_naam_and_beschrijving():
    service = BronService()
    with pytest.raises(ValueError) as exc_info:
        service.create_bron("", "")
    assert str(exc_info.value) == "Naam en beschrijving zijn vereist."