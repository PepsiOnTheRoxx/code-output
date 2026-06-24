import pytest
from src.linkvtproceseigenaar import VernietigingstaakRelatiesService
from src.linkvtproceseigenaar_exceptions import (
    GebruikerNietGevondenException,
    TaakNietGevondenException,
    ProceseigenaarAlGekoppeldException,
    OngeldigeRelatieException,
)

@pytest.fixture
def service():
    return VernietigingstaakRelatiesService()

def test_koppel_proceseigenaar_succesvol(service):
    gebruiker_id = 1
    vernietigingstaak_id = 100
    resultaat = service.koppel_proceseigenaar(gebruiker_id, vernietigingstaak_id)
    assert resultaat is True
    assert service.is_proceseigenaar(gebruiker_id, vernietigingstaak_id) is True

def test_koppel_proceseigenaar_2de_keer_geeft_exception(service):
    gebruiker_id = 2
    vernietigingstaak_id = 200
    service.koppel_proceseigenaar(gebruiker_id, vernietigingstaak_id)
    with pytest.raises(ProceseigenaarAlGekoppeldException):
        service.koppel_proceseigenaar(gebruiker_id, vernietigingstaak_id)

def test_koppel_proceseigenaar_voor_onbekende_gebruiker(service):
    onbekende_gebruiker_id = 999
    vernietigingstaak_id = 300
    with pytest.raises(GebruikerNietGevondenException):
        service.koppel_proceseigenaar(onbekende_gebruiker_id, vernietigingstaak_id)

def test_koppel_proceseigenaar_voor_onbekende_taak(service):
    gebruiker_id = 3
    onbekende_taak_id = 9999
    with pytest.raises(TaakNietGevondenException):
        service.koppel_proceseigenaar(gebruiker_id, onbekende_taak_id)

def test_koppel_proceseigenaar_met_ongeldige_parameters(service):
    with pytest.raises(OngeldigeRelatieException):
        service.koppel_proceseigenaar(None, None)

def test_controleren_of_proceseigenaar_gekoppeld_is(service):
    gebruiker_id = 4
    vernietigingstaak_id = 400
    assert service.is_proceseigenaar(gebruiker_id, vernietigingstaak_id) is False
    service.koppel_proceseigenaar(gebruiker_id, vernietigingstaak_id)
    assert service.is_proceseigenaar(gebruiker_id, vernietigingstaak_id) is True