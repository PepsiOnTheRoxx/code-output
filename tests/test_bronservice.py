import pytest

class BronService:
    class Bron:
        def __init__(self, naam, beschrijving):
            self.naam = naam
            self.beschrijving = beschrijving

    class InvalidBronException(Exception):
        pass

    def create_bron(self, naam, beschrijving):
        if not naam or not beschrijving:
            raise self.InvalidBronException("Naam en beschrijving moeten ingevuld zijn.")
        return self.Bron(naam, beschrijving)


def test_create_bron_met_geldige_gegeven_waarden():
    service = BronService()
    bron = service.create_bron("Test Bron", "Dit is een beschrijving.")
    assert bron.naam == "Test Bron"
    assert bron.beschrijving == "Dit is een beschrijving."


def test_create_bron_met_leeg_naam():
    service = BronService()
    with pytest.raises(BronService.InvalidBronException, match="Naam en beschrijving moeten ingevuld zijn."):
        service.create_bron("", "Een beschrijving.")


def test_create_bron_met_leeg_beschrijving():
    service = BronService()
    with pytest.raises(BronService.InvalidBronException, match="Naam en beschrijving moeten ingevuld zijn."):
        service.create_bron("Een naam", "")


def test_create_bron_met_leeg_naam_en_beschrijving():
    service = BronService()
    with pytest.raises(BronService.InvalidBronException, match="Naam en beschrijving moeten ingevuld zijn."):
        service.create_bron("", "")


def test_create_bron_met_speciale_tekens():
    service = BronService()
    bron = service.create_bron("Bron @#$_&*", "Dit is een beschrijving met speciale tekens #$%&.")
    assert bron.naam == "Bron @#$_&*"
    assert bron.beschrijving == "Dit is een beschrijving met speciale tekens #$%&."