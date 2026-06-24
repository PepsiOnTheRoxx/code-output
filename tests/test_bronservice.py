import pytest
from src.bronservice import BronService

@pytest.fixture
def bron_service():
    return BronService()

@pytest.fixture
def bestaande_bron():
    return {
        "id": 1,
        "naam": "Oude Bron",
        "attribuut_15": "waarde_oude",
        "attribuut_16": 123
    }

def test_update_bron_success(bron_service, bestaande_bron):
    bron_service.add_bron(bestaande_bron)
    nieuwe_gegevens = {
        "naam": "Nieuwe Bron",
        "attribuut_15": "waarde_nieuw",
        "attribuut_16": 456
    }
    result = bron_service.update_bron(1, nieuwe_gegevens)
    assert result is True
    bron = bron_service.get_bron(1)
    assert bron["naam"] == "Nieuwe Bron"
    assert bron["attribuut_15"] == "waarde_nieuw"
    assert bron["attribuut_16"] == 456

def test_update_bron_nonexistent(bron_service):
    nieuwe_gegevens = {
        "naam": "Niet bestaande Bron",
        "attribuut_15": "waarde",
        "attribuut_16": 999
    }
    result = bron_service.update_bron(9999, nieuwe_gegevens)
    assert result is False

def test_update_bron_partial_update(bron_service, bestaande_bron):
    bron_service.add_bron(bestaande_bron)
    nieuwe_gegevens = {
        "naam": "Partiële Bron"
    }
    result = bron_service.update_bron(1, nieuwe_gegevens)
    assert result is True
    bron = bron_service.get_bron(1)
    assert bron["naam"] == "Partiële Bron"
    assert bron["attribuut_15"] == "waarde_oude"
    assert bron["attribuut_16"] == 123

def test_update_bron_invalid_data(bron_service, bestaande_bron):
    bron_service.add_bron(bestaande_bron)
    nieuwe_gegevens = {
        "attribuut_16": "ongeldige_waarde"
    }
    with pytest.raises(ValueError):
        bron_service.update_bron(1, nieuwe_gegevens)