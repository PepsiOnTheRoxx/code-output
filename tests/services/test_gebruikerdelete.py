import pytest
from src.services.gebruikerdelete import GebruikerService
from src.services.gebruikerdelete_exceptions import GebruikerBestaatNietException, VerwijderNietToegestaanException

@pytest.fixture
def gebruiker_service():
    service = GebruikerService()
    return service

def test_verwijder_bestaande_gebruiker(monkeypatch, gebruiker_service):
    def dummy_verwijder(id):
        return True
    monkeypatch.setattr(gebruiker_service, '_verwijder_gebruiker', dummy_verwijder)
    gebruiker_id = 42
    resultaat = gebruiker_service.verwijder(gebruiker_id)
    assert resultaat is True

def test_verwijder_gebruiker_niet_bestaat(monkeypatch, gebruiker_service):
    def dummy_verwijder(id):
        raise GebruikerBestaatNietException
    monkeypatch.setattr(gebruiker_service, '_verwijder_gebruiker', dummy_verwijder)
    gebruiker_id = 100
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_niet_toegestaan(monkeypatch, gebruiker_service):
    def dummy_verwijder(id):
        raise VerwijderNietToegestaanException
    monkeypatch.setattr(gebruiker_service, '_verwijder_gebruiker', dummy_verwijder)
    gebruiker_id = 23
    with pytest.raises(VerwijderNietToegestaanException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_geen_side_effect_bij_fout(monkeypatch, gebruiker_service):
    def dummy_verwijder(id):
        raise GebruikerBestaatNietException
    monkeypatch.setattr(gebruiker_service, '_verwijder_gebruiker', dummy_verwijder)
    gebruiker_id = 77
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_met_meerdere_calls(monkeypatch, gebruiker_service):
    # Simuleer side effect: eerste keer True, tweede keer exception
    calls = [True, GebruikerBestaatNietException()]
    def dummy_verwijder(id):
        res = calls.pop(0)
        if isinstance(res, Exception):
            raise res
        return res
    monkeypatch.setattr(gebruiker_service, '_verwijder_gebruiker', dummy_verwijder)
    gebruiker_id_1 = 10
    gebruiker_id_2 = 20
    resultaat = gebruiker_service.verwijder(gebruiker_id_1)
    assert resultaat is True
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id_2)
