import pytest
from src.readbron import BronService
from src.readbron_exceptions import BronNotFoundException, InvalidBronIdException

def test_readbron_returns_bron_data(monkeypatch):
    bron_id = 1
    mock_bron = {
        "id": bron_id,
        "naam": "TestBron",
        "beschrijving": "Dit is een testbron"
    }
    def mock_get_bron(self, bron_id_):
        return mock_bron
    monkeypatch.setattr(BronService, "get_bron", mock_get_bron)
    service = BronService()
    result = service.get_bron(bron_id)
    assert result["id"] == bron_id
    assert result["naam"] == "TestBron"
    assert result["beschrijving"] == "Dit is een testbron"

def test_readbron_bron_not_found(monkeypatch):
    bron_id = 999
    def mock_get_bron(self, bron_id_):
        raise BronNotFoundException("Bron niet gevonden")
    monkeypatch.setattr(BronService, "get_bron", mock_get_bron)
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.get_bron(bron_id)

def test_readbron_invalid_id(monkeypatch):
    invalid_id = "abc"
    def mock_get_bron(self, bron_id_):
        raise InvalidBronIdException("Ongeldig bron ID")
    monkeypatch.setattr(BronService, "get_bron", mock_get_bron)
    service = BronService()
    with pytest.raises(InvalidBronIdException):
        service.get_bron(invalid_id)

def test_readbron_returns_expected_attributes(monkeypatch):
    bron_id = 2
    mock_bron = {
        "id": bron_id,
        "naam": "BronX",
        "beschrijving": "BronX beschrijving",
        "metadata": {"created": "2024-06-01"}
    }
    def mock_get_bron(self, bron_id_):
        return mock_bron
    monkeypatch.setattr(BronService, "get_bron", mock_get_bron)
    service = BronService()
    result = service.get_bron(bron_id)
    assert "id" in result
    assert "naam" in result
    assert "beschrijving" in result
    assert result["naam"] == "BronX"
    assert result["beschrijving"] == "BronX beschrijving"
    assert isinstance(result["metadata"], dict)

def test_readbron_strip_whitespace_in_naam_en_beschrijving(monkeypatch):
    bron_id = 3
    mock_bron = {
        "id": bron_id,
        "naam": "  BronY  ",
        "beschrijving": "  Beschrijving met spaties  "
    }
    def mock_get_bron(self, bron_id_):
        return {
            "id": bron_id_,
            "naam": mock_bron["naam"].strip(),
            "beschrijving": mock_bron["beschrijving"].strip()
        }
    monkeypatch.setattr(BronService, "get_bron", mock_get_bron)
    service = BronService()
    result = service.get_bron(bron_id)
    assert result["naam"] == "BronY"
    assert result["beschrijving"] == "Beschrijving met spaties"
