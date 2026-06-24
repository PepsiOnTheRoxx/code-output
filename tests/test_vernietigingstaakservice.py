import pytest
from src.vernietigingstaakservice import VernietigingstaakService, Vernietigingstaak

@pytest.fixture
def service():
    return VernietigingstaakService()

@pytest.fixture
def bestaande_taak():
    return Vernietigingstaak(id=1, naam="Taak1", status="Aangemaakt", omschrijving="Omschrijving1")

def test_update_vernietigingstaak_succes(service, bestaande_taak):
    service.taken = {1: bestaande_taak}
    update_data = {
        "naam": "Taak1 Gewijzigd",
        "status": "In Uitvoering",
        "omschrijving": "Gewijzigde omschrijving"
    }
    taak = service.update_vernietigingstaak(1, update_data)
    assert taak.naam == "Taak1 Gewijzigd"
    assert taak.status == "In Uitvoering"
    assert taak.omschrijving == "Gewijzigde omschrijving"

def test_update_vernietigingstaak_bestaat_niet(service):
    update_data = {
        "naam": "Taak2",
        "status": "In Uitvoering",
        "omschrijving": "Omschrijving2"
    }
    with pytest.raises(KeyError):
        service.update_vernietigingstaak(999, update_data)

def test_update_vernietigingstaak_partial_update(service, bestaande_taak):
    service.taken = {1: bestaande_taak}
    update_data = {
        "status": "Voltooid"
    }
    taak = service.update_vernietigingstaak(1, update_data)
    assert taak.status == "Voltooid"
    assert taak.naam == "Taak1"
    assert taak.omschrijving == "Omschrijving1"

def test_update_vernietigingstaak_invalid_attribute(service, bestaande_taak):
    service.taken = {1: bestaande_taak}
    update_data = {
        "onbestaande_attribuut": "waarde"
    }
    taak = service.update_vernietigingstaak(1, update_data)
    assert not hasattr(taak, "onbestaande_attribuut")
    assert taak.naam == "Taak1"
    assert taak.status == "Aangemaakt"
    assert taak.omschrijving == "Omschrijving1"

def test_update_vernietigingstaak_empty_update(service, bestaande_taak):
    service.taken = {1: bestaande_taak}
    update_data = {}
    taak = service.update_vernietigingstaak(1, update_data)
    assert taak.naam == "Taak1"
    assert taak.status == "Aangemaakt"
    assert taak.omschrijving == "Omschrijving1"