import pytest
from src.services.vtarchivarisrelatiemanagement import VTArchivarisRelatieService
from src.services.vtarchivarisrelatiemanagement_exceptions import (
    RelatieBestaatAlException,
    RelatieNietGevondenException,
    OngeldigeInputException
)

@pytest.fixture
def relatie_service():
    return VTArchivarisRelatieService()

def test_voeg_relatie_toe_succes(relatie_service):
    vernietigingstaak_id = 1
    gebruiker_id = 100
    relatie_service.voeg_relatie_toe(vernietigingstaak_id, gebruiker_id)
    relaties = relatie_service.lijst_relaties(vernietigingstaak_id)
    assert gebruiker_id in relaties

def test_voeg_relatie_toe_al_bestaand(relatie_service):
    vernietigingstaak_id = 2
    gebruiker_id = 101
    relatie_service.voeg_relatie_toe(vernietigingstaak_id, gebruiker_id)
    with pytest.raises(RelatieBestaatAlException):
        relatie_service.voeg_relatie_toe(vernietigingstaak_id, gebruiker_id)

def test_verwijder_bestaande_relatie(relatie_service):
    vernietigingstaak_id = 3
    gebruiker_id = 102
    relatie_service.voeg_relatie_toe(vernietigingstaak_id, gebruiker_id)
    relatie_service.verwijder_relatie(vernietigingstaak_id, gebruiker_id)
    relaties = relatie_service.lijst_relaties(vernietigingstaak_id)
    assert gebruiker_id not in relaties

def test_verwijder_niet_bestaande_relatie(relatie_service):
    vernietigingstaak_id = 4
    gebruiker_id = 103
    with pytest.raises(RelatieNietGevondenException):
        relatie_service.verwijder_relatie(vernietigingstaak_id, gebruiker_id)

def test_lijst_relaties_meerdere_gebruikers(relatie_service):
    vernietigingstaak_id = 5
    gebruiker_ids = [104, 105, 106]
    for gebruiker_id in gebruiker_ids:
        relatie_service.voeg_relatie_toe(vernietigingstaak_id, gebruiker_id)
    relaties = relatie_service.lijst_relaties(vernietigingstaak_id)
    assert set(relaties) == set(gebruiker_ids)

def test_lijst_relaties_geen_gekoppeld(relatie_service):
    vernietigingstaak_id = 6
    relaties = relatie_service.lijst_relaties(vernietigingstaak_id)
    assert relaties == []

def test_voeg_relatie_toe_ongeldige_input(relatie_service):
    with pytest.raises(OngeldigeInputException):
        relatie_service.voeg_relatie_toe(None, 200)
    with pytest.raises(OngeldigeInputException):
        relatie_service.voeg_relatie_toe(7, None)

def test_verwijder_relatie_ongeldige_input(relatie_service):
    with pytest.raises(OngeldigeInputException):
        relatie_service.verwijder_relatie(None, 201)
    with pytest.raises(OngeldigeInputException):
        relatie_service.verwijder_relatie(8, None)

def test_lijst_relaties_ongeldige_input(relatie_service):
    with pytest.raises(OngeldigeInputException):
        relatie_service.lijst_relaties(None)
