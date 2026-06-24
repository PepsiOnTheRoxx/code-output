import pytest
from src.gebruikerservice import GebruikerService, GebruikerNietGevondenFout

@pytest.fixture
def gebruiker_service():
    service = GebruikerService()
    service.voeg_gebruiker_toe('jan', 'Jan Jansen', 'jan@voorbeeld.nl')
    service.voeg_gebruiker_toe('piet', 'Piet Pietersen', 'piet@voorbeeld.nl')
    return service

def test_verwijder_bestaande_gebruiker(gebruiker_service):
    assert gebruiker_service.bestaat_gebruiker('jan')
    gebruiker_service.verwijder_gebruiker('jan')
    assert not gebruiker_service.bestaat_gebruiker('jan')

def test_verwijder_andere_gebruiker_blijft_bestaan(gebruiker_service):
    gebruiker_service.verwijder_gebruiker('jan')
    assert gebruiker_service.bestaat_gebruiker('piet')

def test_verwijder_niet_bestaande_gebruiker_geeft_fout(gebruiker_service):
    with pytest.raises(GebruikerNietGevondenFout):
        gebruiker_service.verwijder_gebruiker('klaas')

def test_verwijder_gebruiker_meerdere_keer(gebruiker_service):
    gebruiker_service.verwijder_gebruiker('jan')
    with pytest.raises(GebruikerNietGevondenFout):
        gebruiker_service.verwijder_gebruiker('jan')

def test_verwijder_gebruiker_met_leeg_id(gebruiker_service):
    with pytest.raises(GebruikerNietGevondenFout):
        gebruiker_service.verwijder_gebruiker('')