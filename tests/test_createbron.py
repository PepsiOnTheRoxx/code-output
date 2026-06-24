import pytest
from src.createbron import BronService
from src.createbron_exceptions import BronAlreadyExistsException, InvalidBronNameException, InvalidBronDescriptionException

@pytest.fixture
def bron_service():
    return BronService()

def test_create_bron_success(bron_service):
    naam = "Waterput"
    beschrijving = "Een bron in het bos."
    bron = bron_service.create_bron(naam, beschrijving)
    assert bron.naam == naam
    assert bron.beschrijving == beschrijving
    assert bron.id is not None

def test_create_bron_already_exists(bron_service):
    naam = "Waterput"
    beschrijving = "Een bron in het bos."
    bron_service.create_bron(naam, beschrijving)
    with pytest.raises(BronAlreadyExistsException):
        bron_service.create_bron(naam, "Andere beschrijving")

@pytest.mark.parametrize("naam", [None, "", "    "])
def test_create_bron_invalid_naam(bron_service, naam):
    with pytest.raises(InvalidBronNameException):
        bron_service.create_bron(naam, "Goede beschrijving")

@pytest.mark.parametrize("beschrijving", [None, "", "    "])
def test_create_bron_invalid_beschrijving(bron_service, beschrijving):
    with pytest.raises(InvalidBronDescriptionException):
        bron_service.create_bron("Heidebron", beschrijving)

def test_create_multiple_brons_unique_names(bron_service):
    bron1 = bron_service.create_bron("Duinbron", "Bron bij de duinen")
    bron2 = bron_service.create_bron("Heidebron", "Bron op de heide")
    assert bron1.naam != bron2.naam
    assert bron1.id != bron2.id