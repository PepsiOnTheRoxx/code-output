import pytest
from src.services.bronupdate import BronService
from src.services.bronupdate_exceptions import BronNotFoundException, InvalidBronDataException

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

def test_update_bron_succesvol(bron_service, bestaande_bron, mocker):
    nieuwe_gegevens = {
        'naam': 'Bron A - Gewijzigd',
        'omschrijving': 'Gewijzigde omschrijving'
    }
    mock_get = mocker.patch.object(bron_service, 'get_bron_by_id', return_value=bestaande_bron)
    mock_save = mocker.patch.object(bron_service, 'save_bron')
    result = bron_service.update_bron(bestaande_bron['id'], nieuwe_gegevens)
    mock_get.assert_called_once_with(bestaande_bron['id'])
    mock_save.assert_called_once()
    assert result['naam'] == 'Bron A - Gewijzigd'
    assert result['omschrijving'] == 'Gewijzigde omschrijving'
    assert result['id'] == bestaande_bron['id']

def test_update_bron_niet_bestaand(bron_service, mocker):
    niet_bestaand_id = 99
    nieuwe_gegevens = {'naam': 'Nieuw'}
    mocker.patch.object(bron_service, 'get_bron_by_id', return_value=None)
    with pytest.raises(BronNotFoundException):
        bron_service.update_bron(niet_bestaand_id, nieuwe_gegevens)

def test_update_bron_ongeldige_data(bron_service, bestaande_bron, mocker):
    ongeldige_data = {'naam': ''}  # Verplichte 'naam' mag niet leeg zijn
    mocker.patch.object(bron_service, 'get_bron_by_id', return_value=bestaande_bron)
    with pytest.raises(InvalidBronDataException):
        bron_service.update_bron(bestaande_bron['id'], ongeldige_data)

def test_update_bron_behoudt_ongewijzigde_velden(bron_service, bestaande_bron, mocker):
    partiele_update = {'omschrijving': 'Nieuwe omschrijving'}
    expected_bron = bestaande_bron.copy()
    expected_bron['omschrijving'] = 'Nieuwe omschrijving'
    mocker.patch.object(bron_service, 'get_bron_by_id', return_value=bestaande_bron)
    mock_save = mocker.patch.object(bron_service, 'save_bron')
    result = bron_service.update_bron(bestaande_bron['id'], partiele_update)
    mock_save.assert_called_once()
    assert result['naam'] == bestaande_bron['naam']
    assert result['omschrijving'] == 'Nieuwe omschrijving'
    assert result['type'] == bestaande_bron['type']

def test_update_bron_elementtype_check(bron_service, bestaande_bron, mocker):
    verkeerde_type_data = {'type': 'IncorrectType'}
    mocker.patch.object(bron_service, 'get_bron_by_id', return_value=bestaande_bron)
    with pytest.raises(InvalidBronDataException):
        bron_service.update_bron(bestaande_bron['id'], verkeerde_type_data)