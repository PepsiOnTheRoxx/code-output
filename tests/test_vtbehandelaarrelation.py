import pytest
from src.vtbehandelaarrelation import DestructionTaskService, Gebruiker, Vernietigingstaak, VTBehandelaarRelationException

@pytest.fixture
def gebruiker():
    return Gebruiker(id=1, naam="Jan")

@pytest.fixture
def tweede_gebruiker():
    return Gebruiker(id=2, naam="Piet")

@pytest.fixture
def taak():
    return Vernietigingstaak(id=100, omschrijving="Taak A")

@pytest.fixture
def tweede_taak():
    return Vernietigingstaak(id=200, omschrijving="Taak B")

@pytest.fixture
def service():
    return DestructionTaskService()

def test_koppel_behandelaar_succes(service, gebruiker, taak):
    assert service.koppel_behandelaar(gebruiker, taak) is True
    assert service.is_behandelaar(gebruiker, taak)

def test_koppel_meerdere_behandelaars_aan_taak(service, gebruiker, tweede_gebruiker, taak):
    service.koppel_behandelaar(gebruiker, taak)
    service.koppel_behandelaar(tweede_gebruiker, taak)
    assert service.is_behandelaar(gebruiker, taak)
    assert service.is_behandelaar(tweede_gebruiker, taak)

def test_koppel_behandelaar_aan_meerdere_taken(service, gebruiker, taak, tweede_taak):
    service.koppel_behandelaar(gebruiker, taak)
    service.koppel_behandelaar(gebruiker, tweede_taak)
    assert service.is_behandelaar(gebruiker, taak)
    assert service.is_behandelaar(gebruiker, tweede_taak)

def test_behandelaar_al_gekoppeld_throws(service, gebruiker, taak):
    service.koppel_behandelaar(gebruiker, taak)
    with pytest.raises(VTBehandelaarRelationException):
        service.koppel_behandelaar(gebruiker, taak)

def test_ontkoppel_behandelaar_succes(service, gebruiker, taak):
    service.koppel_behandelaar(gebruiker, taak)
    assert service.ontkoppel_behandelaar(gebruiker, taak) is True
    assert not service.is_behandelaar(gebruiker, taak)

def test_ontkoppel_niet_gekoppelde_behandelaar_throws(service, gebruiker, taak):
    with pytest.raises(VTBehandelaarRelationException):
        service.ontkoppel_behandelaar(gebruiker, taak)

def test_is_behandelaar_false_for_unlinked(service, gebruiker, taak):
    assert not service.is_behandelaar(gebruiker, taak)

def test_get_behandelaars_for_taak(service, gebruiker, tweede_gebruiker, taak):
    service.koppel_behandelaar(gebruiker, taak)
    service.koppel_behandelaar(tweede_gebruiker, taak)
    behandelaars = service.get_behandelaars(taak)
    assert gebruiker in behandelaars
    assert tweede_gebruiker in behandelaars
    assert len(behandelaars) == 2

def test_get_taken_for_behandelaar(service, gebruiker, taak, tweede_taak):
    service.koppel_behandelaar(gebruiker, taak)
    service.koppel_behandelaar(gebruiker, tweede_taak)
    taken = service.get_taken(gebruiker)
    assert taak in taken
    assert tweede_taak in taken
    assert len(taken) == 2