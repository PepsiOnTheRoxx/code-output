import pytest
from unittest.mock import MagicMock, patch
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

@pytest.fixture
def boek_service():
    return BoekService()

def test_update_boek_succesvol(boek_service):
    boek_id = 1
    bestaande_boek = MagicMock()
    nieuwe_data = {"titel": "Nieuwe Titel", "auteur": "Nieuwe Auteur"}
    with patch.object(boek_service, 'get_boek_by_id', return_value=bestaande_boek) as mock_get, \
         patch.object(bestaande_boek, 'update', return_value=None) as mock_update, \
         patch.object(boek_service, 'save_boek', return_value=bestaande_boek) as mock_save:
        resultaat = boek_service.update_boek(boek_id, nieuwe_data)
        mock_get.assert_called_once_with(boek_id)
        mock_update.assert_called_once_with(nieuwe_data)
        mock_save.assert_called_once_with(bestaande_boek)
        assert resultaat == bestaande_boek

def test_update_boek_bestaat_niet(boek_service):
    boek_id = 99
    nieuwe_data = {"titel": "Nieuwe Titel"}
    with patch.object(boek_service, 'get_boek_by_id', return_value=None):
        with pytest.raises(BoekNietGevondenException):
            boek_service.update_boek(boek_id, nieuwe_data)

def test_update_boek_ongeldige_data(boek_service):
    boek_id = 2
    bestaande_boek = MagicMock()
    nieuwe_data = {"titel": ""}  # Ongeldige titel
    with patch.object(boek_service, 'get_boek_by_id', return_value=bestaande_boek), \
         patch.object(bestaande_boek, 'update', side_effect=OngeldigeBoekDataException):
        with pytest.raises(OngeldigeBoekDataException):
            boek_service.update_boek(boek_id, nieuwe_data)

def test_update_boek_save_faalt(boek_service):
    boek_id = 3
    bestaande_boek = MagicMock()
    nieuwe_data = {"titel": "Titel"}
    with patch.object(boek_service, 'get_boek_by_id', return_value=bestaande_boek), \
         patch.object(bestaande_boek, 'update', return_value=None), \
         patch.object(boek_service, 'save_boek', side_effect=Exception("Save failed")):
        with pytest.raises(Exception) as exc_info:
            boek_service.update_boek(boek_id, nieuwe_data)
        assert "Save failed" in str(exc_info.value)

def test_update_boek_partial_update(boek_service):
    boek_id = 4
    bestaande_boek = MagicMock()
    oude_titel = "Oude Titel"
    nieuwe_data = {"titel": "Nieuwe Titel"}
    bestaande_boek.titel = oude_titel
    with patch.object(boek_service, 'get_boek_by_id', return_value=bestaande_boek), \
         patch.object(bestaande_boek, 'update', return_value=None) as mock_update, \
         patch.object(boek_service, 'save_boek', return_value=bestaande_boek):
        boek_service.update_boek(boek_id, nieuwe_data)
        mock_update.assert_called_once_with(nieuwe_data)