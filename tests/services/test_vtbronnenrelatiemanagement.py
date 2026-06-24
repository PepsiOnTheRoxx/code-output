import pytest
from src.services.vtbronnenrelatiemanagement import VTBronnenRelatieService
from src.services.vtbronnenrelatiemanagement_exceptions import (
    KoppelingBestaatAlException,
    KoppelingNietGevondenException,
    OngeldigeBronException,
    OngeldigeVernietigingstaakException
)

@pytest.fixture
def service():
    return VTBronnenRelatieService()

def test_koppeling_toevoegen_succesvol(service):
    vernietigingstaak_id = 1
    bron_id = 10
    koppeling = service.koppeling_toevoegen(vernietigingstaak_id, bron_id)
    assert koppeling['vernietigingstaak_id'] == vernietigingstaak_id
    assert koppeling['bron_id'] == bron_id

def test_koppeling_toevoegen_bestaat_al(service):
    vernietigingstaak_id = 2
    bron_id = 20
    service.koppeling_toevoegen(vernietigingstaak_id, bron_id)
    with pytest.raises(KoppelingBestaatAlException):
        service.koppeling_toevoegen(vernietigingstaak_id, bron_id)

def test_koppeling_toevoegen_ongeldige_bron(service):
    vernietigingstaak_id = 3
    ongeldige_bron_id = 'xyz'
    with pytest.raises(OngeldigeBronException):
        service.koppeling_toevoegen(vernietigingstaak_id, ongeldige_bron_id)

def test_koppeling_toevoegen_ongeldige_vernietigingstaak(service):
    ongeldige_vernietigingstaak_id = None
    bron_id = 30
    with pytest.raises(OngeldigeVernietigingstaakException):
        service.koppeling_toevoegen(ongeldige_vernietigingstaak_id, bron_id)

def test_koppeling_verwijderen_succesvol(service):
    vernietigingstaak_id = 4
    bron_id = 40
    service.koppeling_toevoegen(vernietigingstaak_id, bron_id)
    service.koppeling_verwijderen(vernietigingstaak_id, bron_id)
    with pytest.raises(KoppelingNietGevondenException):
        service.koppeling_verwijderen(vernietigingstaak_id, bron_id)

def test_koppeling_verwijderen_niet_gevonden(service):
    vernietigingstaak_id = 5
    bron_id = 50
    with pytest.raises(KoppelingNietGevondenException):
        service.koppeling_verwijderen(vernietigingstaak_id, bron_id)

def test_lijst_koppelingen_empty(service):
    vernietigingstaak_id = 6
    koppelingen = service.lijst_koppelingen(vernietigingstaak_id)
    assert koppelingen == []

def test_lijst_koppelingen_multiple(service):
    vernietigingstaak_id = 7
    bron_ids = [100, 101, 102]
    for bron_id in bron_ids:
        service.koppeling_toevoegen(vernietigingstaak_id, bron_id)
    koppelingen = service.lijst_koppelingen(vernietigingstaak_id)
    returned_bron_ids = [k['bron_id'] for k in koppelingen]
    assert set(returned_bron_ids) == set(bron_ids)
