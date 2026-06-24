import pytest
from src.services.bronupdate import BronService
from src.services.bronupdate_exceptions import BronNietGevondenException, OngeldigeBronDataException

@pytest.fixture
def bron_service():
    return BronService()

@pytest.fixture
def bestaande_bron():
    return {
        'id': 1,
        'naam': 'Bron A',
        'omschrijving': 'Oude omschrijving',
        'type': 'ObjectType',
        'element_id': 12
    }

def test_update_bron_succesvol(bron_service, bestaande_bron, monkeypatch):
    nieuwe_gegevens = {
        'naam': 'Bron A - Gewijzigd',
        'omschrijving': 'Gewijzigde omschrijving'
    }
    def mock_get(bron_id):
        return bestaande_bron
    def mock_save(bron):
        pass
    monkeypatch.setattr(bron_service, 'get_bron_by_id', mock_get)
    monkeypatch.setattr(bron_service, 'save_bron', mock_save)
    result = bron_service.update_bron(bestaande_bron['id'], nieuwe_gegevens)
    assert result['naam'] == 'Bron A - Gewijzigd'
    assert result['omschrijving'] == 'Gewijzigde omschrijving'
    assert result['id'] == bestaande_bron['id']

def test_update_bron_niet_bestaand(bron_service, monkeypatch):
    niet_bestaand_id = 99
    nieuwe_gegevens = {'naam': 'Nieuw'}
    def mock_get(bron_id):
        return None
    monkeypatch.setattr(bron_service, 'get_bron_by_id', mock_get)
    with pytest.raises(BronNietGevondenException):
        bron_service.update_bron(niet_bestaand_id, nieuwe_gegevens)

def test_update_bron_ongeldige_data(bron_service, bestaande_bron, monkeypatch):
    ongeldige_data = {'naam': ''}  # Verplichte 'naam' mag niet leeg zijn
    def mock_get(bron_id):
        return bestaande_bron
    monkeypatch.setattr(bron_service, 'get_bron_by_id', mock_get)
    with pytest.raises(OngeldigeBronDataException):
        bron_service.update_bron(bestaande_bron['id'], ongeldige_data)

def test_update_bron_behoudt_ongewijzigde_velden(bron_service, bestaande_bron, monkeypatch):
    partiele_update = {'omschrijving': 'Nieuwe omschrijving'}
    expected_bron = bestaande_bron.copy()
    expected_bron['omschrijving'] = 'Nieuwe omschrijving'
    def mock_get(bron_id):
        return bestaande_bron
    def mock_save(bron):
        pass
    monkeypatch.setattr(bron_service, 'get_bron_by_id', mock_get)
    monkeypatch.setattr(bron_service, 'save_bron', mock_save)
    result = bron_service.update_bron(bestaande_bron['id'], partiele_update)
    assert result['naam'] == bestaande_bron['naam']
    assert result['omschrijving'] == 'Nieuwe omschrijving'
    assert result['type'] == bestaande_bron['type']

def test_update_bron_elementtype_check(bron_service, bestaande_bron, monkeypatch):
    verkeerde_type_data = {'type': 'IncorrectType'}
    def mock_get(bron_id):
        return bestaande_bron
    monkeypatch.setattr(bron_service, 'get_bron_by_id', mock_get)
    with pytest.raises(OngeldigeBronDataException):
        bron_service.update_bron(bestaande_bron['id'], verkeerde_type_data)
