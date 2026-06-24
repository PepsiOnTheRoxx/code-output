import pytest
from src.services.vtbehandelaarrelatiemanagement import VTBehandelaarRelatieService
from src.services.vtbehandelaarrelatiemanagement_exceptions import (
    OngeldigeVernietigingstaakException as VernietigingstaakNotFoundException,
    OngeldigeBehandelaarException as GebruikerNotFoundException,
    BehandelaarKoppelingBestaatAlException as RelatieAlreadyExistsException,
    BehandelaarKoppelingNietGevondenException as RelatieNotFoundException,
)

@pytest.fixture
def service():
    return VTBehandelaarRelatieService()

def test_koppel_behandelaar_succesvol(service):
    vernietigingstaak_id = 1
    gebruiker_id = 10
    relatie = service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id)
    assert relatie.vernietigingstaak_id == vernietigingstaak_id
    assert relatie.gebruiker_id == gebruiker_id

def test_koppel_behandelaar_vernietigingstaak_bestaat_niet(service):
    vernietigingstaak_id = 9999
    gebruiker_id = 10
    with pytest.raises(VernietigingstaakNotFoundException):
        service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id)

def test_koppel_behandelaar_gebruiker_bestaat_niet(service):
    vernietigingstaak_id = 1
    gebruiker_id = 9999
    with pytest.raises(GebruikerNotFoundException):
        service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id)

def test_koppel_behandelaar_reeds_bestaande_relatie(service):
    vernietigingstaak_id = 1
    gebruiker_id = 10
    service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id)
    with pytest.raises(RelatieAlreadyExistsException):
        service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id)

def test_verwijder_behandelaar_succesvol(service):
    vernietigingstaak_id = 1
    gebruiker_id = 10
    service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id)
    service.verwijder_behandelaar(vernietigingstaak_id, gebruiker_id)
    relaties = service.lijst_behandelaars(vernietigingstaak_id)
    assert gebruiker_id not in [r.gebruiker_id for r in relaties]

def test_verwijder_behandelaar_relatie_bestaat_niet(service):
    vernietigingstaak_id = 1
    gebruiker_id = 10
    with pytest.raises(RelatieNotFoundException):
        service.verwijder_behandelaar(vernietigingstaak_id, gebruiker_id)

def test_lijst_behandelaars_leeg(service):
    vernietigingstaak_id = 1
    relaties = service.lijst_behandelaars(vernietigingstaak_id)
    assert isinstance(relaties, list)
    assert len(relaties) == 0

def test_lijst_behandelaars_na_koppelen(service):
    vernietigingstaak_id = 1
    gebruiker_id1 = 10
    gebruiker_id2 = 11
    service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id1)
    service.koppel_behandelaar(vernietigingstaak_id, gebruiker_id2)
    relaties = service.lijst_behandelaars(vernietigingstaak_id)
    gebruiker_ids = [r.gebruiker_id for r in relaties]
    assert set(gebruiker_ids) == {gebruiker_id1, gebruiker_id2}

def test_lijst_behandelaars_vernietigingstaak_bestaat_niet(service):
    vernietigingstaak_id = 9999
    with pytest.raises(VernietigingstaakNotFoundException):
        service.lijst_behandelaars(vernietigingstaak_id)
