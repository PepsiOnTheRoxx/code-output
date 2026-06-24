import pytest
from src.gebruikerservice import GebruikerService

@pytest.fixture
def service():
    return GebruikerService()

def test_create_gebruiker_success(service):
    email = "test@voorbeeld.nl"
    naam = "Test Gebruiker"
    gebruiker = service.create_gebruiker(email, naam)
    assert gebruiker.emailadres == email
    assert gebruiker.naam == naam
    assert hasattr(gebruiker, "id")

def test_create_gebruiker_missing_email(service):
    naam = "Test Gebruiker"
    with pytest.raises(ValueError):
        service.create_gebruiker(None, naam)

def test_create_gebruiker_missing_naam(service):
    email = "test@voorbeeld.nl"
    with pytest.raises(ValueError):
        service.create_gebruiker(email, None)

def test_create_gebruiker_invalid_email_format(service):
    naam = "Test Gebruiker"
    invalid_email = "geenemailformaat"
    with pytest.raises(ValueError):
        service.create_gebruiker(invalid_email, naam)

def test_create_gebruiker_duplicate_email(service):
    email = "test@voorbeeld.nl"
    naam1 = "Gebruiker 1"
    naam2 = "Gebruiker 2"
    service.create_gebruiker(email, naam1)
    with pytest.raises(ValueError):
        service.create_gebruiker(email, naam2)