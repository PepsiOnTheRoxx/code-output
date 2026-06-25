import pytest
from unittest.mock import patch, MagicMock
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

def test_update_boek_succesvol():
    boek_id = 1
    bestaande_boek = MagicMock()
    geupdate_boek = MagicMock()
    update_data = {'titel': 'Nieuwe Titel', 'auteur': 'Nieuwe Auteur'}

    with patch('src.services.boekupdate.BoekRepository') as MockRepo:
        mock_repo = MockRepo.return_value
        mock_repo.get_boek_by_id.return_value = bestaande_boek
        mock_repo.update_boek.return_value = geupdate_boek

        service = BoekService(mock_repo)
        resultaat = service.update_boek(boek_id, update_data)

        mock_repo.get_boek_by_id.assert_called_once_with(boek_id)
        mock_repo.update_boek.assert_called_once_with(bestaande_boek, update_data)
        assert resultaat == geupdate_boek

def test_update_boek_niet_gevonden():
    boek_id = 999
    update_data = {'titel': 'Titel'}
    with patch('src.services.boekupdate.BoekRepository') as MockRepo:
        mock_repo = MockRepo.return_value
        mock_repo.get_boek_by_id.return_value = None

        service = BoekService(mock_repo)
        with pytest.raises(BoekNietGevondenException):
            service.update_boek(boek_id, update_data)

        mock_repo.get_boek_by_id.assert_called_once_with(boek_id)
        mock_repo.update_boek.assert_not_called()

def test_update_boek_ongeldige_data():
    boek_id = 2
    bestaande_boek = MagicMock()
    update_data = {'titel': ''}  # stel lege titel is ongeldig

    with patch('src.services.boekupdate.BoekRepository') as MockRepo:
        mock_repo = MockRepo.return_value
        mock_repo.get_boek_by_id.return_value = bestaande_boek
        mock_repo.update_boek.side_effect = OngeldigeBoekDataException()

        service = BoekService(mock_repo)
        with pytest.raises(OngeldigeBoekDataException):
            service.update_boek(boek_id, update_data)

        mock_repo.get_boek_by_id.assert_called_once_with(boek_id)
        mock_repo.update_boek.assert_called_once_with(bestaande_boek, update_data)

def test_update_boek_partial_update():
    boek_id = 3
    bestaande_boek = MagicMock()
    geupdate_boek = MagicMock()
    update_data = {'titel': 'Aanpassing'}

    with patch('src.services.boekupdate.BoekRepository') as MockRepo:
        mock_repo = MockRepo.return_value
        mock_repo.get_boek_by_id.return_value = bestaande_boek
        mock_repo.update_boek.return_value = geupdate_boek

        service = BoekService(mock_repo)
        resultaat = service.update_boek(boek_id, update_data)

        mock_repo.get_boek_by_id.assert_called_once_with(boek_id)
        mock_repo.update_boek.assert_called_once_with(bestaande_boek, update_data)
        assert resultaat == geupdate_boek

def test_update_boek_opslag_faalt():
    boek_id = 4
    bestaande_boek = MagicMock()
    update_data = {'titel': 'Titel Fout'}

    with patch('src.services.boekupdate.BoekRepository') as MockRepo:
        mock_repo = MockRepo.return_value
        mock_repo.get_boek_by_id.return_value = bestaande_boek
        mock_repo.update_boek.side_effect = Exception("Opslag mislukt")

        service = BoekService(mock_repo)
        with pytest.raises(Exception) as exc_info:
            service.update_boek(boek_id, update_data)

        assert "Opslag mislukt" in str(exc_info.value)
        mock_repo.get_boek_by_id.assert_called_once_with(boek_id)
        mock_repo.update_boek.assert_called_once_with(bestaande_boek, update_data)