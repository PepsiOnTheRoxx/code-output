import pytest
from unittest.mock import patch
from src.services.vtproceseigenaarrelatie import VTProceseigenaarRelatieService
from src.services.vtproceseigenaarrelatie_exceptions import (
    ProceseigenaarNietGevondenException,
    VernietigingstaakNietGevondenException,
    ProceseigenaarRelatieBestaatAlException,
    ProceseigenaarRelatieNietGevondenException
)

@pytest.fixture
def service():
    return VTProceseigenaarRelatieService()

def test_koppel_proceseigenaar_succesvol(service):
    gebruiker_id = 10
    taak_id = 20
    # Directe call (geen patch, test de echte code)
    result = service.koppel_proceseigenaar(gebruiker_id, taak_id)
    assert result is True
    # Koppeling is gelegd
    proceseigenaren = service.get_proceseigenaren_voor_taak(taak_id)
    assert any(p['id'] == gebruiker_id for p in proceseigenaren)

def test_koppel_proceseigenaar_gebruiker_bestaat_niet(service):
    gebruiker_id = 999
    taak_id = 20
    with pytest.raises(ProceseigenaarNietGevondenException):
        service.koppel_proceseigenaar(gebruiker_id, taak_id)

def test_koppel_proceseigenaar_taak_bestaat_niet(service):
    gebruiker_id = 5
    taak_id = 1234567
    with pytest.raises(VernietigingstaakNietGevondenException):
        service.koppel_proceseigenaar(gebruiker_id, taak_id)

def test_koppel_proceseigenaar_reeds_gekoppeld(service):
    gebruiker_id = 12
    taak_id = 30
    service.koppel_proceseigenaar(gebruiker_id, taak_id)
    with pytest.raises(ProceseigenaarRelatieBestaatAlException):
        service.koppel_proceseigenaar(gebruiker_id, taak_id)

def test_verwijder_proceseigenaarrelatie_succesvol(service):
    gebruiker_id = 7
    taak_id = 33
    service.koppel_proceseigenaar(gebruiker_id, taak_id)
    # Verwijderen
    service.verwijder_proceseigenaarrelatie(gebruiker_id, taak_id)
    assert gebruiker_id not in [p['id'] for p in service.get_proceseigenaren_voor_taak(taak_id)]

def test_verwijder_proceseigenaarrelatie_niet_gevonden(service):
    gebruiker_id = 99
    taak_id = 100
    with pytest.raises(ProceseigenaarRelatieNietGevondenException):
        service.verwijder_proceseigenaarrelatie(gebruiker_id, taak_id)

def test_get_proceseigenaren_voor_taak(service):
    taak_id = 50
    service.koppel_proceseigenaar(1, taak_id)
    service.koppel_proceseigenaar(2, taak_id)
    result = service.get_proceseigenaren_voor_taak(taak_id)
    assert {'id': 1, 'naam': 'Piet'} in result
    assert {'id': 2, 'naam': 'Klaas'} in result
    assert len(result) == 2

def test_get_taken_voor_proceseigenaar(service):
    gebruiker_id = 25
    service.koppel_proceseigenaar(gebruiker_id, 101)
    service.koppel_proceseigenaar(gebruiker_id, 102)
    result = service.get_taken_voor_proceseigenaar(gebruiker_id)
    assert {'id': 101, 'omschrijving': 'Taak A'} in result
    assert {'id': 102, 'omschrijving': 'Taak B'} in result
    assert len(result) == 2
