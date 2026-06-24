import pytest
from src.deletegebruiker import GebruikerService
from src.deletegebruiker_exceptions import GebruikerNietGevondenException, GebruikerVerwijderenNietToegestaanException, GebruikerDeleteDatabaseFoutException

@pytest.fixture
def gebruiker_service():
    return GebruikerService()

def test_verwijder_gebruiker_succes(gebruiker_service, monkeypatch):
    gebruiker_id = 42
    monkeypatch.setattr(gebruiker_service, "bestaat_gebruiker", lambda gid: True)
    monkeypatch.setattr(gebruiker_service, "mag_verwijderen", lambda gid: True)
    monkeypatch.setattr(gebruiker_service, "verwijder_gebruiker_uit_db", lambda gid: None)

    gebruiker_service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_gebruiker_niet_gevonden(gebruiker_service, monkeypatch):
    gebruiker_id = 43
    monkeypatch.setattr(gebruiker_service, "bestaat_gebruiker", lambda gid: False)

    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_gebruiker_ongeautoriseerd(gebruiker_service, monkeypatch):
    gebruiker_id = 44
    monkeypatch.setattr(gebruiker_service, "bestaat_gebruiker", lambda gid: True)
    monkeypatch.setattr(gebruiker_service, "mag_verwijderen", lambda gid: False)

    with pytest.raises(GebruikerVerwijderenNietToegestaanException):
        gebruiker_service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_gebruiker_db_fout(gebruiker_service, monkeypatch):
    gebruiker_id = 45
    monkeypatch.setattr(gebruiker_service, "bestaat_gebruiker", lambda gid: True)
    monkeypatch.setattr(gebruiker_service, "mag_verwijderen", lambda gid: True)
    def raise_db_exception(gid):
        raise GebruikerDeleteDatabaseFoutException()
    monkeypatch.setattr(gebruiker_service, "verwijder_gebruiker_uit_db", raise_db_exception)

    with pytest.raises(GebruikerDeleteDatabaseFoutException):
        gebruiker_service.verwijder_gebruiker(gebruiker_id)
