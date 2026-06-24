import pytest
from src.services.gebruikerdelete import GebruikerService
from src.services.gebruikerdelete_exceptions import GebruikerBestaatNietException, VerwijderNietToegestaanException

@pytest.fixture
def gebruiker_service():
    # Reset "db" voor elke test
    service = GebruikerService()
    service._gebruikers_db = {
        10: {'mag_verwijderen': True},
        20: {'mag_verwijderen': False},
        23: {'mag_verwijderen': False},
        42: {'mag_verwijderen': True},
        77: {'mag_verwijderen': True},
    }
    return service

def test_verwijder_bestaande_gebruiker(gebruiker_service):
    gebruiker_id = 42
    resultaat = gebruiker_service.verwijder(gebruiker_id)
    assert resultaat is True
    assert 42 not in gebruiker_service._gebruikers_db

def test_verwijder_gebruiker_niet_bestaat(gebruiker_service):
    gebruiker_id = 100
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_niet_toegestaan(gebruiker_service):
    gebruiker_id = 23
    with pytest.raises(VerwijderNietToegestaanException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_geen_side_effect_bij_fout(gebruiker_service):
    gebruiker_id = 77
    # Eerste keer verwijderen OK
    gebruiker_service.verwijder(gebruiker_id)
    # Tweede keer bestaat gebruiker niet meer en moet exception geven
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_met_meerdere_calls(gebruiker_service):
    gebruiker_id_1 = 10  # mag verwijderen
    gebruiker_id_2 = 20  # verwijderd niet toegestaan
    resultaat = gebruiker_service.verwijder(gebruiker_id_1)
    assert resultaat is True
    with pytest.raises(VerwijderNietToegestaanException):
        gebruiker_service.verwijder(gebruiker_id_2)
