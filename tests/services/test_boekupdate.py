import pytest
from unittest.mock import patch, MagicMock
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

@pytest.fixture
def mock_boek_repo():
    with patch('src.services.boekupdate.BoekRepository') as MockRepo:
        yield MockRepo.return_value

@pytest.fixture
def boek_service(mock_boek_repo):
    return BoekService(mock_boek_repo)

def test_update_boek_succesvol(boek_service, mock_boek_repo):
    bestaand_boek = MagicMock()
    mock_boek_repo.get_boek_by_id.return_value = bestaand_boek
    nieuwe_data = {'titel': 'Nieuwe titel', 'auteur': 'Nieuwe auteur'}
    boek_service.update_boek(1, nieuwe_data)
    mock_boek_repo.get_boek_by_id.assert_called_once_with(1)
    assert bestaand_boek.titel == 'Nieuwe titel'
    assert bestaand_boek.auteur == 'Nieuwe auteur'
    mock_boek_repo.save_boek.assert_called_once_with(bestaand_boek)

def test_update_boek_niet_gevonden(boek_service, mock_boek_repo):
    mock_boek_repo.get_boek_by_id.return_value = None
    with pytest.raises(BoekNietGevondenException):
        boek_service.update_boek(99, {'titel': 'Test'})

def test_update_boek_ongeldige_data(boek_service, mock_boek_repo):
    bestaand_boek = MagicMock()
    mock_boek_repo.get_boek_by_id.return_value = bestaand_boek
    with pytest.raises(OngeldigeBoekDataException):
        boek_service.update_boek(1, {'titel': ''})

def test_update_boek_partial_update(boek_service, mock_boek_repo):
    bestaand_boek = MagicMock()
    bestaand_boek.titel = 'Oud Titel'
    bestaand_boek.auteur = 'Oud Auteur'
    mock_boek_repo.get_boek_by_id.return_value = bestaand_boek
    nieuwe_data = {'auteur': 'Nieuw Auteur'}
    boek_service.update_boek(1, nieuwe_data)
    assert bestaand_boek.titel == 'Oud Titel'
    assert bestaand_boek.auteur == 'Nieuw Auteur'
    mock_boek_repo.save_boek.assert_called_once_with(bestaand_boek)

def test_update_boek_repo_save_fout(boek_service, mock_boek_repo):
    bestaand_boek = MagicMock()
    mock_boek_repo.get_boek_by_id.return_value = bestaand_boek
    mock_boek_repo.save_boek.side_effect = Exception("Opslaan mislukt")
    with pytest.raises(Exception, match="Opslaan mislukt"):
        boek_service.update_boek(1, {'titel': 'Titel', 'auteur': 'Auteur'})