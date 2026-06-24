import pytest
from src.services.managevtbehandelaarrelatie import VTBehandelaarRelatieService
from src.services.managevtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieAlreadyExists,
    VTBehandelaarRelatieNotFound,
    InvalidVTBehandelaarRelatieData,
)

@pytest.fixture
def service():
    return VTBehandelaarRelatieService()

def test_voeg_behandelaar_toe_succesvol(service):
    gebruiker_id = 1
    vernietigingstaak_id = 20
    result = service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)
    assert result is True
    assert service.get_behandelaars_by_taak(vernietigingstaak_id) == [gebruiker_id]
    assert service.get_taken_by_behandelaar(gebruiker_id) == [vernietigingstaak_id]

def test_voeg_behandelaar_toe_bestaat_al_exception(service):
    gebruiker_id = 1
    vernietigingstaak_id = 20
    service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)
    with pytest.raises(VTBehandelaarRelatieAlreadyExists):
        service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)

def test_voeg_behandelaar_toe_ongeldige_behandelaar_exception(service):
    gebruiker_id = 99
    vernietigingstaak_id = 21
    with pytest.raises(InvalidVTBehandelaarRelatieData):
        service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)

def test_verwijder_behandelaar_succesvol(service):
    gebruiker_id = 2
    vernietigingstaak_id = 15
    service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)
    result = service.verwijder_behandelaar(gebruiker_id, vernietigingstaak_id)
    assert result is True
    assert service.get_behandelaars_by_taak(vernietigingstaak_id) == []
    assert service.get_taken_by_behandelaar(gebruiker_id) == []

def test_verwijder_behandelaar_niet_gevonden_exception(service):
    gebruiker_id = 3
    vernietigingstaak_id = 18
    with pytest.raises(VTBehandelaarRelatieNotFound):
        service.verwijder_behandelaar(gebruiker_id, vernietigingstaak_id)

def test_get_behandelaars_by_taak_succesvol(service):
    vernietigingstaak_id = 40
    behandelaars = [10, 11, 12]
    for b in behandelaars:
        service.voeg_behandelaar_toe(b, vernietigingstaak_id)
    result = sorted(service.get_behandelaars_by_taak(vernietigingstaak_id))
    assert sorted(behandelaars) == result

def test_get_taken_by_behandelaar_succesvol(service):
    gebruiker_id = 4
    taken = [100, 101]
    for t in taken:
        service.voeg_behandelaar_toe(gebruiker_id, t)
    result = sorted(service.get_taken_by_behandelaar(gebruiker_id))
    assert sorted(taken) == result

def test_get_behandelaars_by_taak_geen_behandelaars(service):
    vernietigingstaak_id = 41
    result = service.get_behandelaars_by_taak(vernietigingstaak_id)
    assert result == []
