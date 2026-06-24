import pytest
from unittest.mock import patch, MagicMock
from src.services.bronupdate import BronService, Bron
from src.services.bronupdate_exceptions import BronUpdateNotFoundException, BronUpdateValidationException

@pytest.fixture
def bron_service():
    service = BronService()
    # Vul met testdata
    BronService._bron_db = {
        1: Bron(1, naam='Oude', type='bron'),
        2: Bron(2, naam='Oude Naam', type='water'),
        3: Bron(3, naam='Test3', type='vuur')
    }
    return service

def test_update_existing_bron_success(bron_service):
    bron_id = 1
    nieuwe_data = {'naam': 'Nieuwe Naam', 'type': 'water'}
    oude_bron = bron_service.get_bron_by_id(bron_id)
    with patch.object(bron_service, 'get_bron_by_id', return_value=oude_bron) as mock_get, \
         patch.object(bron_service, 'validate_data', return_value=True) as mock_validate, \
         patch.object(bron_service, 'save_bron') as mock_save:
        bron_service.update_bron(bron_id, nieuwe_data)
        mock_get.assert_called_once_with(bron_id)
        mock_validate.assert_called_once_with(nieuwe_data)
        assert oude_bron.naam == 'Nieuwe Naam'
        assert oude_bron.type == 'water'
        mock_save.assert_called_once_with(oude_bron)

def test_update_bron_not_found(bron_service):
    bron_id = 99
    nieuwe_data = {'naam': 'X', 'type': 'y'}
    with patch.object(bron_service, 'get_bron_by_id', return_value=None):
        with pytest.raises(BronUpdateNotFoundException):
            bron_service.update_bron(bron_id, nieuwe_data)

def test_update_bron_invalid_data(bron_service):
    bron_id = 1
    nieuwe_data = {'naam': ''}  # Ongeldige data
    oude_bron = MagicMock()
    with patch.object(bron_service, 'get_bron_by_id', return_value=oude_bron), \
         patch.object(bron_service, 'validate_data', side_effect=BronUpdateValidationException):
        with pytest.raises(BronUpdateValidationException):
            bron_service.update_bron(bron_id, nieuwe_data)

def test_update_existing_bron_partial_data(bron_service):
    bron_id = 2
    nieuwe_data = {'type': 'lucht'}
    oude_bron = bron_service.get_bron_by_id(bron_id)
    with patch.object(bron_service, 'get_bron_by_id', return_value=oude_bron), \
         patch.object(bron_service, 'validate_data', return_value=True), \
         patch.object(bron_service, 'save_bron') as mock_save:
        bron_service.update_bron(bron_id, nieuwe_data)
        assert oude_bron.naam == 'Oude Naam'
        assert oude_bron.type == 'lucht'
        mock_save.assert_called_once_with(oude_bron)

def test_update_bron_save_fails(bron_service):
    bron_id = 3
    nieuwe_data = {'naam': 'Test', 'type': 'vuur'}
    oude_bron = bron_service.get_bron_by_id(bron_id)
    with patch.object(bron_service, 'get_bron_by_id', return_value=oude_bron), \
         patch.object(bron_service, 'validate_data', return_value=True), \
         patch.object(bron_service, 'save_bron', side_effect=Exception("DB fout")):
        with pytest.raises(Exception) as excinfo:
            bron_service.update_bron(bron_id, nieuwe_data)
        assert "DB fout" in str(excinfo.value)
