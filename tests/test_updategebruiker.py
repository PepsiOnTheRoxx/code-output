import pytest
from src.updategebruiker import GebruikerService
from src.updategebruiker_exceptions import (
    GebruikerNietGevondenException,
    OngeldigeGebruikersgegevensException,
    UpdateNietToegestaanException
)

@pytest.fixture
def gebruiker_data():
    return {
        "id": 1,
        "naam": "Jan",
        "email": "jan@email.com"
    }

@pytest.fixture
def service(mocker, gebruiker_data):
    mock_repo = mocker.Mock()
    mock_repo.get_by_id.return_value = gebruiker_data.copy()
    mock_repo.update.return_value = None
    return GebruikerService(repository=mock_repo)

def test_update_gebruiker_succesvol(service, gebruiker_data):
    nieuwe_gegevens = {"naam": "Klaas", "email": "klaas@email.com"}
    resultaat = service.update_gebruiker(gebruiker_data["id"], nieuwe_gegevens)
    assert resultaat["naam"] == "Klaas"
    assert resultaat["email"] == "klaas@email.com"
    service.repository.update.assert_called_once_with(gebruiker_data["id"], nieuwe_gegevens)

def test_update_gebruiker_niet_gevonden(mocker):
    mock_repo = mocker.Mock()
    mock_repo.get_by_id.return_value = None
    service = GebruikerService(repository=mock_repo)
    with pytest.raises(GebruikerNietGevondenException):
        service.update_gebruiker(99, {"naam": "Piet"})

def test_update_gebruiker_ongeldige_gegevens(service, gebruiker_data):
    ongeldige_gegevens = {"naam": "", "email": "niet-an-email"}
    service.repository.get_by_id.return_value = gebruiker_data.copy()
    with pytest.raises(OngeldigeGebruikersgegevensException):
        service.update_gebruiker(gebruiker_data["id"], ongeldige_gegevens)

def test_update_niet_toegestaan(service, gebruiker_data, mocker):
    service.repository.get_by_id.return_value = gebruiker_data.copy()
    service.mag_bewerken = mocker.Mock(return_value=False)
    with pytest.raises(UpdateNietToegestaanException):
        service.update_gebruiker(gebruiker_data["id"], {"naam": "Nieuwe Naam"})

def test_update_gebruiker_delegeert_naar_repository(service, gebruiker_data):
    nieuwe_gegevens = {"naam": "Lisa", "email": "lisa@email.com"}
    service.update_gebruiker(gebruiker_data["id"], nieuwe_gegevens)
    service.repository.update.assert_called_once_with(gebruiker_data["id"], nieuwe_gegevens)