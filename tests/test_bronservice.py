import pytest
from src.bronservice import BronService

@pytest.fixture
def bron_service():
    return BronService()

def test_create_bron_success(bron_service):
    naam = "Bron 1"
    beschrijving = "Dit is een testbron."
    bron = bron_service.create_bron(naam, beschrijving)
    assert bron is not None
    assert bron["Naam"] == naam
    assert bron["Beschrijving"] == beschrijving

def test_create_bron_missing_naam(bron_service):
    beschrijving = "Bron zonder naam."
    with pytest.raises(ValueError):
        bron_service.create_bron(None, beschrijving)

def test_create_bron_empty_naam(bron_service):
    beschrijving = "Bron met lege naam."
    with pytest.raises(ValueError):
        bron_service.create_bron("", beschrijving)

def test_create_bron_missing_beschrijving(bron_service):
    naam = "Bron zonder beschrijving"
    with pytest.raises(ValueError):
        bron_service.create_bron(naam, None)

def test_create_bron_duplicate_naam(bron_service):
    naam = "Bron Duplicaat"
    beschrijving = "Eerste bron"
    bron_service.create_bron(naam, beschrijving)
    with pytest.raises(ValueError):
        bron_service.create_bron(naam, "Tweede bron met dezelfde naam")

def test_create_bron_trims_inputs(bron_service):
    naam = "  Bron met spaties  "
    beschrijving = "  Beschrijving met spaties  "
    bron = bron_service.create_bron(naam, beschrijving)
    assert bron["Naam"] == naam.strip()
    assert bron["Beschrijving"] == beschrijving.strip()

def test_create_bron_metamodel_elements(bron_service):
    naam = "BronMeta"
    beschrijving = "Metamodel test"
    bron = bron_service.create_bron(naam, beschrijving)
    assert bron["ElementType"] == "ObjectType"
    assert "ElementID" in bron