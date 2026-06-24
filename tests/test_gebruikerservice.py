import pytest
from src.gebruikerservice import GebruikerService, Gebruiker

@pytest.fixture
def gebruiker_service():
    return GebruikerService()

@pytest.fixture
def bestaande_gebruiker():
    return Gebruiker(id=1, naam="Jan", email="jan@example.com")

def test_update_gebruiker_succes(gebruiker_service, bestaande_gebruiker):
    gebruiker_service.add_gebruiker(bestaande_gebruiker)
    updated_data = {"naam": "Jan Bijgewerkt", "email": "jan.bijgewerkt@example.com"}
    updated_gebruiker = gebruiker_service.update_gebruiker(1, updated_data)
    assert updated_gebruiker.naam == "Jan Bijgewerkt"
    assert updated_gebruiker.email == "jan.bijgewerkt@example.com"

def test_update_gebruiker_partial_update(gebruiker_service, bestaande_gebruiker):
    gebruiker_service.add_gebruiker(bestaande_gebruiker)
    updated_data = {"naam": "Jan Nieuw"}
    updated_gebruiker = gebruiker_service.update_gebruiker(1, updated_data)
    assert updated_gebruiker.naam == "Jan Nieuw"
    assert updated_gebruiker.email == "jan@example.com"

def test_update_gebruiker_nonexistent(gebruiker_service):
    with pytest.raises(KeyError):
        gebruiker_service.update_gebruiker(42, {"naam": "Onbekend"})

def test_update_gebruiker_invalid_attribute(gebruiker_service, bestaande_gebruiker):
    gebruiker_service.add_gebruiker(bestaande_gebruiker)
    updated_data = {"adres": "Straat 1"}
    with pytest.raises(AttributeError):
        gebruiker_service.update_gebruiker(1, updated_data)

def test_update_gebruiker_empty_update(gebruiker_service, bestaande_gebruiker):
    gebruiker_service.add_gebruiker(bestaande_gebruiker)
    updated_gebruiker = gebruiker_service.update_gebruiker(1, {})
    assert updated_gebruiker.naam == "Jan"
    assert updated_gebruiker.email == "jan@example.com"