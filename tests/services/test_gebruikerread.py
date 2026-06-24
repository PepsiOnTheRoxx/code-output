import pytest
from src.services.gebruikerread import GebruikerService
from src.services.gebruikerread_exceptions import GebruikerNietGevondenException

@pytest.fixture
def gebruiker_data():
    return {
        1: {"id": 1, "naam": "Jan Jansen", "email": "jan.jansen@example.com"},
        2: {"id": 2, "naam": "Piet Pieters", "email": "piet.pieters@example.com"},
    }

@pytest.fixture
def gebruiker_service(monkeypatch, gebruiker_data):
    service = GebruikerService()
    monkeypatch.setattr(service, "_gebruikers", gebruiker_data)
    return service

def test_lees_bestaande_gebruiker_succes(gebruiker_service):
    gebruiker = gebruiker_service.lees_gebruiker(1)
    assert gebruiker["id"] == 1
    assert gebruiker["naam"] == "Jan Jansen"
    assert gebruiker["email"] == "jan.jansen@example.com"

def test_lees_andere_bestaande_gebruiker(gebruiker_service):
    gebruiker = gebruiker_service.lees_gebruiker(2)
    assert gebruiker["id"] == 2
    assert gebruiker["naam"] == "Piet Pieters"
    assert gebruiker["email"] == "piet.pieters@example.com"

def test_lees_onbestaande_gebruiker_werpt_exception(gebruiker_service):
    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.lees_gebruiker(999)

def test_lees_gebruiker_met_none_id_werpt_exception(gebruiker_service):
    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.lees_gebruiker(None)

def test_lees_gebruiker_met_negatief_id(gebruiker_service):
    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.lees_gebruiker(-10)

def test_lees_gebruiker_met_string_id_werpt_exception(gebruiker_service):
    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.lees_gebruiker("abc")
