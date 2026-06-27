import pytest
from unittest.mock import patch, MagicMock
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNotFoundException, InvalidBoekDataException

@pytest.fixture
def boek_service():
    return BoekService()

def test_update_boek_succesvol(boek_service):
    mock_boek = MagicMock()
    update_data = {'titel': 'Nieuwe Titel'}
    with patch.object(boek_service, 'get_boek_by_id', return_value=mock_boek) as mock_get, \
         patch.object(boek_service, 'save_boek') as mock_save:
        updated_boek = boek_service.update_boek(1, update_data)
        mock_get.assert_called_once_with(1)
        mock_boek.titel = 'Nieuwe Titel'
        mock_save.assert_called_once_with(mock_boek)
        assert updated_boek == mock_boek

def test_update_boek_niet_gevonden(boek_service):
    with patch.object(boek_service, 'get_boek_by_id', return_value=None):
        with pytest.raises(BoekNotFoundException):
            boek_service.update_boek(99, {'titel': 'Onbestaand Boek'})

def test_update_boek_ongeldige_data(boek_service):
    mock_boek = MagicMock()
    ongeldige_data = {'titel': ''}  # Stel lege titel is ongeldig
    with patch.object(boek_service, 'get_boek_by_id', return_value=mock_boek):
        with pytest.raises(InvalidBoekDataException):
            boek_service.update_boek(2, ongeldige_data)

def test_update_boek_partial_update(boek_service):
    mock_boek = MagicMock()
    mock_boek.titel = 'Oude Titel'
    update_data = {'titel': 'Nieuwe Titel'}
    with patch.object(boek_service, 'get_boek_by_id', return_value=mock_boek), \
         patch.object(boek_service, 'save_boek') as mock_save:
        updated_boek = boek_service.update_boek(3, update_data)
        assert mock_boek.titel == 'Nieuwe Titel'
        mock_save.assert_called_once_with(mock_boek)
        assert updated_boek == mock_boek

def test_update_boek_onverwachte_fout(boek_service):
    with patch.object(boek_service, 'get_boek_by_id', side_effect=Exception('Database Down')):
        with pytest.raises(Exception) as exc_info:
            boek_service.update_boek(4, {'titel': 'Titel'})
        assert 'Database Down' in str(exc_info.value)
