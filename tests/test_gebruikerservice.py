import pytest

class Gebruiker:
    def __init__(self, email, naam):
        if not self.is_valid_email(email):
            raise ValueError("Ongeldig emailadres.")
        self.email = email
        self.naam = naam

    @staticmethod
    def is_valid_email(email):
        return "@" in email

class GebruikerService:
    def create_gebruiker(self, email, naam):
        return Gebruiker(email, naam)

def test_create_gebruiker_met_valide_gegevens():
    service = GebruikerService()
    gebruiker = service.create_gebruiker("test@example.com", "Test Naam")
    assert gebruiker.email == "test@example.com"
    assert gebruiker.naam == "Test Naam"

def test_create_gebruiker_met_ongeldig_emailadres():
    service = GebruikerService()
    with pytest.raises(ValueError, match="Ongeldig emailadres."):
        service.create_gebruiker("ongeldig_emailadres", "Test Naam")

def test_create_gebruiker_met_nameloze_gebruiker():
    service = GebruikerService()
    gebruiker = service.create_gebruiker("test@example.com", "")
    assert gebruiker.email == "test@example.com"
    assert gebruiker.naam == ""

def test_create_gebruiker_met_speciale_tekens_in_naam():
    service = GebruikerService()
    gebruiker = service.create_gebruiker("test@example.com", "Test Naam!@#")
    assert gebruiker.email == "test@example.com"
    assert gebruiker.naam == "Test Naam!@#"