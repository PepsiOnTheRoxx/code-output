import pytest
from src.services.bronread import BronService
from src.services.bronread_exceptions import BronNotFoundException, BronReadException

@pytest.fixture
def bronservice():
    return BronService()

def test_lees_bestaande_bron_succes(bronservice):
    bron_id = 1
    bron = bronservice.lees_bron(bron_id)
    assert bron is not None
    assert bron["id"] == bron_id
    assert "naam" in bron

def test_lees_bestaande_bron_inhoud(bronservice):
    bron_id = 2
    bron = bronservice.lees_bron(bron_id)
    assert isinstance(bron, dict)
    assert bron.get("id") == bron_id
    assert isinstance(bron.get("naam"), str)
    assert isinstance(bron.get("type"), str) or bron.get("type") is None

def test_lees_bron_niet_bestaand(bronservice):
    niet_bestaand_id = 99999
    with pytest.raises(BronNotFoundException):
        bronservice.lees_bron(niet_bestaand_id)

def test_lees_bron_invalid_id(bronservice):
    invalid_id = "ongeldig"
    with pytest.raises(BronReadException):
        bronservice.lees_bron(invalid_id)

def test_lees_bron_none_id(bronservice):
    with pytest.raises(BronReadException):
        bronservice.lees_bron(None)

def test_lees_bron_exception_handling(bronservice, monkeypatch):
    # vervang alleen de _lees_bron, niet de wrapper/exceptionhandler
    def raise_generic_exception(self, _):
        raise Exception("Onverwachte fout")
    monkeypatch.setattr(BronService, "_lees_bron", raise_generic_exception)
    with pytest.raises(BronReadException):
        bronservice.lees_bron(3)
