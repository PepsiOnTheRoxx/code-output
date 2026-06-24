import pytest
from src.services.creategebruiker import GebruikerService
from src.services.creategebruiker_exceptions import GebruikerAlreadyExistsException, InvalidGebruikerDataException

def test_create_gebruiker_succesvol_aanmaken():
    service = GebruikerService()
    gebruiker_data = {
        "naam": "Jan Jansen",
        "emailadres": "jan.jansen@example.com"
    }
    gebruiker = service.create_gebruiker(gebruiker_data)
    assert gebruiker is not None
    assert gebruiker.naam == "Jan Jansen"
    assert gebruiker.emailadres == "jan.jansen@example.com"

def test_create_gebruiker_bestaat_al():
    service = GebruikerService()
    gebruiker_data = {
        "naam": "Piet Pieters",
        "emailadres": "piet.pieters@example.com"
    }
    service.create_gebruiker(gebruiker_data)
    with pytest.raises(GebruikerAlreadyExistsException):
        service.create_gebruiker(gebruiker_data)

def test_create_gebruiker_ongeldig_emailadres():
    service = GebruikerService()
    gebruiker_data = {
        "naam": "Klaas Klaassen",
        "emailadres": "klaas.klaassen"  # Ongeldig emailadres
    }
    with pytest.raises(InvalidGebruikerDataException):
        service.create_gebruiker(gebruiker_data)

def test_create_gebruiker_missing_emailadres():
    service = GebruikerService()
    gebruiker_data = {
        "naam": "Sara Smit"
        # Geen emailadres
    }
    with pytest.raises(InvalidGebruikerDataException):
        service.create_gebruiker(gebruiker_data)

def test_create_gebruiker_leeg_naamveld():
    service = GebruikerService()
    gebruiker_data = {
        "naam": "",
        "emailadres": "leeg.naam@example.com"
    }
    gebruiker = service.create_gebruiker(gebruiker_data)
    assert gebruiker.naam == ""
    assert gebruiker.emailadres == "leeg.naam@example.com"
