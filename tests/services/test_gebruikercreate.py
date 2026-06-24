import pytest
from src.services.gebruikercreate import GebruikerService
from src.services.gebruikercreate_exceptions import EmailAdresBestaatAlException, OngeldigEmailAdresException, OngeldigeNaamException

@pytest.fixture
def gebruiker_service():
    return GebruikerService()

def test_gebruiker_create_succes(gebruiker_service):
    naam = "Jan Jansen"
    email = "jan.jansen@example.com"
    gebruiker = gebruiker_service.maak_gebruiker(naam, email)
    assert gebruiker.naam == naam
    assert gebruiker.email == email

def test_gebruiker_create_email_bestaat_al(gebruiker_service):
    naam = "Piet Pietersen"
    email = "piet.pietersen@example.com"
    gebruiker_service.maak_gebruiker(naam, email)
    with pytest.raises(EmailAdresBestaatAlException):
        gebruiker_service.maak_gebruiker("Andere Naam", email)

def test_gebruiker_create_ongeldig_emailadres(gebruiker_service):
    naam = "Klaas Klaassen"
    ongeldig_email = "klaas.klaassen@"
    with pytest.raises(OngeldigEmailAdresException):
        gebruiker_service.maak_gebruiker(naam, ongeldig_email)

def test_gebruiker_create_lege_naam(gebruiker_service):
    lege_naam = ""
    geldig_email = "test.naam@example.com"
    with pytest.raises(OngeldigeNaamException):
        gebruiker_service.maak_gebruiker(lege_naam, geldig_email)

def test_gebruiker_create_naam_alleen_spaties(gebruiker_service):
    naam_spaties = "   "
    geldig_email = "spatie.naam@example.com"
    with pytest.raises(OngeldigeNaamException):
        gebruiker_service.maak_gebruiker(naam_spaties, geldig_email)