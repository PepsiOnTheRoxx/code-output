import pytest
from src.deletegebruiker import UserService, GebruikerNotFoundException

@pytest.fixture
def user_service():
    service = UserService()
    # Voeg een paar gebruikers toe om in tests te gebruiken
    service.gebruikers = {
        1: {'id': 1, 'naam': 'Alice'},
        2: {'id': 2, 'naam': 'Bob'}
    }
    return service

def test_delete_bestaande_gebruiker(user_service):
    user_service.delete_gebruiker(1)
    assert 1 not in user_service.gebruikers

def test_delete_gebruiker_verwijdert_juiste_gebruiker(user_service):
    user_service.delete_gebruiker(2)
    assert 2 not in user_service.gebruikers
    assert 1 in user_service.gebruikers  # Andere gebruiker blijft bestaan

def test_delete_onbestaande_gebruiker_geeft_exception(user_service):
    with pytest.raises(GebruikerNotFoundException):
        user_service.delete_gebruiker(999)

def test_delete_gebruiker_herhaald_geeft_exception(user_service):
    user_service.delete_gebruiker(1)
    with pytest.raises(GebruikerNotFoundException):
        user_service.delete_gebruiker(1)

def test_delete_gebruiker_verwijdert_niet_andere_gebruikers(user_service):
    user_service.delete_gebruiker(2)
    assert 1 in user_service.gebruikers
    assert 2 not in user_service.gebruikers

def test_delete_gebruiker_leeg_dict():
    service = UserService()
    service.gebruikers = {}
    with pytest.raises(GebruikerNotFoundException):
        service.delete_gebruiker(1)