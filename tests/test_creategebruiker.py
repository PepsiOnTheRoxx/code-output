import pytest
from src.creategebruiker import GebruikerService
from src.creategebruiker_exceptions import GebruikerBestaatAlException, OngeldigEmailadresException

def test_create_gebruiker_succes():
    service = GebruikerService()
    gebruiker = service.create_gebruiker(naam="Jan Jansen", email="jan.jansen@example.com")
    assert gebruiker.naam == "Jan Jansen"
    assert gebruiker.email == "jan.jansen@example.com"

def test_create_gebruiker_bestaat_al():
    service = GebruikerService()
    service.create_gebruiker(naam="Anne", email="anne@example.com")
    with pytest.raises(GebruikerBestaatAlException):
        service.create_gebruiker(naam="Anne", email="anne@example.com")

def test_create_gebruiker_ongeldig_email():
    service = GebruikerService()
    with pytest.raises(OngeldigEmailadresException):
        service.create_gebruiker(naam="Piet", email="niet-een-email")

def test_create_gebruiker_leeg_naam():
    service = GebruikerService()
    with pytest.raises(ValueError):
        service.create_gebruiker(naam="", email="pietje@example.com")

def test_create_gebruiker_leeg_email():
    service = GebruikerService()
    with pytest.raises(ValueError):
        service.create_gebruiker(naam="Klaas", email="")