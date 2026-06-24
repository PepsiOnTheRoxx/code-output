import pytest
from src.updategebruiker import GebruikerService
from src.updategebruiker_exceptions import (
    GebruikerNietGevondenException,
    OngeldigeGebruikersgegevensException,
    UpdateNietToegestaanException
)

class MockRepository:
    def __init__(self, gebruiker=None):
        self._gebruiker = gebruiker
        self.update_calls = []
    def get_by_id(self, user_id):
        return self._gebruiker.copy() if self._gebruiker else None
    def update(self, user_id, nieuwe_gegevens):
        self.update_calls.append((user_id, nieuwe_gegevens))

@pytest.fixture
def gebruiker_data():
    return {
        "id": 1,
        "naam": "Jan",
        "email": "jan@email.com"
    }

@pytest.fixture
def service(gebruiker_data):
    repo = MockRepository(gebruiker=gebruiker_data)
    return GebruikerService(repository=repo)

def test_update_gebruiker_succesvol(service, gebruiker_data):
    nieuwe_gegevens = {"naam": "Klaas", "email": "klaas@email.com"}
    result = service.update_gebruiker(gebruiker_data["id"], nieuwe_gegevens)
    assert result["naam"] == "Klaas"
    assert result["email"] == "klaas@email.com"
    assert service.repository.update_calls == [(gebruiker_data["id"], nieuwe_gegevens)]

def test_update_gebruiker_niet_gevonden():
    repo = MockRepository(gebruiker=None)
    service = GebruikerService(repository=repo)
    with pytest.raises(GebruikerNietGevondenException):
        service.update_gebruiker(99, {"naam": "Piet", "email": "piet@email.com"})

def test_update_gebruiker_ongeldige_gegevens(service, gebruiker_data):
    ongeldige_gegevens = {"naam": "", "email": "niet-an-email"}
    service.repository._gebruiker = gebruiker_data.copy()
    with pytest.raises(OngeldigeGebruikersgegevensException):
        service.update_gebruiker(gebruiker_data["id"], ongeldige_gegevens)

def test_update_niet_toegestaan(service, gebruiker_data):
    # Verruil mag_bewerken voor altijd False
    def always_false(_gebruiker, _nieuwe):
        return False
    service.mag_bewerken = always_false
    with pytest.raises(UpdateNietToegestaanException):
        service.update_gebruiker(gebruiker_data["id"], {"naam": "Nieuwe Naam", "email": "jan@email.com"})

def test_update_gebruiker_delegeert_naar_repository(service, gebruiker_data):
    nieuwe_gegevens = {"naam": "Lisa", "email": "lisa@email.com"}
    service.update_gebruiker(gebruiker_data["id"], nieuwe_gegevens)
    assert service.repository.update_calls == [(gebruiker_data["id"], nieuwe_gegevens)]
