import pytest
from unittest.mock import patch, MagicMock
from src.services.boekupdateservice import BoekService
from src.services.boekupdateservice_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

@pytest.fixture
def boek_data():
    return {
        "id": 1,
        "titel": "Nieuwe Titel",
        "auteur": "Nieuwe Auteur",
        "isbn": "1234567890123"
    }

@pytest.fixture
def oud_boek():
    return MagicMock(id=1, titel="Oude Titel", auteur="Oude Auteur", isbn="9876543219876")

def test_update_boek_succesvol(boek_data, oud_boek):
    with patch("src.services.boekupdateservice.BoekRepository") as MockRepo:
        repo = MockRepo.return_value
        repo.get_boek_by_id.return_value = oud_boek
        repo.update_boek.return_value = None
        service = BoekService(repo)
        service.update_boek(boek_data["id"], boek_data)
        repo.get_boek_by_id.assert_called_once_with(boek_data["id"])
        repo.update_boek.assert_called_once()
        args, kwargs = repo.update_boek.call_args
        assert args[0].titel == boek_data["titel"]
        assert args[0].auteur == boek_data["auteur"]
        assert args[0].isbn == boek_data["isbn"]

def test_update_boek_niet_gevonden(boek_data):
    with patch("src.services.boekupdateservice.BoekRepository") as MockRepo:
        repo = MockRepo.return_value
        repo.get_boek_by_id.return_value = None
        service = BoekService(repo)
        with pytest.raises(BoekNietGevondenException):
            service.update_boek(boek_data["id"], boek_data)
        repo.get_boek_by_id.assert_called_once_with(boek_data["id"])
        repo.update_boek.assert_not_called()

def test_update_boek_ongeldige_data(boek_data, oud_boek):
    ongeldig_data = boek_data.copy()
    ongeldig_data["titel"] = ""  # Titel mag niet leeg zijn
    with patch("src.services.boekupdateservice.BoekRepository") as MockRepo:
        repo = MockRepo.return_value
        repo.get_boek_by_id.return_value = oud_boek
        service = BoekService(repo)
        with pytest.raises(OngeldigeBoekDataException):
            service.update_boek(oud_boek.id, ongeldig_data)
        repo.update_boek.assert_not_called()

def test_update_boek_exception_bij_opslaan(boek_data, oud_boek):
    with patch("src.services.boekupdateservice.BoekRepository") as MockRepo:
        repo = MockRepo.return_value
        repo.get_boek_by_id.return_value = oud_boek
        repo.update_boek.side_effect = Exception("DB fout")
        service = BoekService(repo)
        with pytest.raises(Exception) as exc:
            service.update_boek(boek_data["id"], boek_data)
        assert "DB fout" in str(exc.value)
        repo.get_boek_by_id.assert_called_once_with(boek_data["id"])
        repo.update_boek.assert_called_once()