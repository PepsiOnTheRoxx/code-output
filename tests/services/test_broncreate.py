import pytest
from src.services.broncreate import BronService
from src.services.broncreate_exceptions import BronCreateDuplicateException, BronCreateInvalidNameException, BronCreateInvalidDescriptionException

@pytest.fixture
def bron_service():
    return BronService()

def test_create_bron_success(bron_service):
    naam = "DataBron"
    beschrijving = "Beschrijving van de bron"
    bron = bron_service.create_bron(naam=naam, beschrijving=beschrijving)
    assert bron.naam == naam
    assert bron.beschrijving == beschrijving
    assert hasattr(bron, "id")

def test_create_bron_missing_naam(bron_service):
    beschrijving = "Beschrijving zonder naam"
    with pytest.raises(BronCreateInvalidNameException):
        bron_service.create_bron(naam=None, beschrijving=beschrijving)

def test_create_bron_missing_beschrijving(bron_service):
    naam = "ZonderBeschrijving"
    with pytest.raises(BronCreateInvalidDescriptionException):
        bron_service.create_bron(naam=naam, beschrijving=None)

def test_create_bron_empty_naam(bron_service):
    beschrijving = "Lege naam"
    with pytest.raises(BronCreateInvalidNameException):
        bron_service.create_bron(naam="", beschrijving=beschrijving)

def test_create_bron_empty_beschrijving(bron_service):
    naam = "LegeBeschrijving"
    with pytest.raises(BronCreateInvalidDescriptionException):
        bron_service.create_bron(naam=naam, beschrijving="")

def test_create_duplicate_bron(bron_service):
    naam = "UniekeBron"
    beschrijving = "Test duplicaat"
    bron_service.create_bron(naam=naam, beschrijving=beschrijving)
    with pytest.raises(BronCreateDuplicateException):
        bron_service.create_bron(naam=naam, beschrijving="Andere beschrijving")

def test_create_bron_special_characters(bron_service):
    naam = "Břön_№1!"
    beschrijving = "Speciaal #$*@!"
    bron = bron_service.create_bron(naam=naam, beschrijving=beschrijving)
    assert bron.naam == naam
    assert bron.beschrijving == beschrijving

def test_create_bron_long_naam_en_beschrijving(bron_service):
    naam = "N" * 255
    beschrijving = "B" * 1024
    bron = bron_service.create_bron(naam=naam, beschrijving=beschrijving)
    assert bron.naam == naam
    assert bron.beschrijving == beschrijving
