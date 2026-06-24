import pytest
from src.services.vtbehandelaarrelatie import VTBehandelaarRelatieService
from src.services.vtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieBestaatAlException,
    VTBehandelaarRelatieNietGevondenException,
    OngeldigeGebruikerException,
    OngeldigeVernietigingstaakException,
)

def setup_module(module):
    VTBehandelaarRelatieService._relaties.clear()

def test_maak_relatie_succesvol():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 10
    taak_id = 20
    assert not service.bestaat_relatie(gebruiker_id, taak_id)
    service.maak_relatie(gebruiker_id, taak_id)
    assert service.bestaat_relatie(gebruiker_id, taak_id)

def test_maak_relatie_bestaat_al():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 11
    taak_id = 21
    service.opslaan_relatie(gebruiker_id, taak_id)
    with pytest.raises(VTBehandelaarRelatieBestaatAlException):
        service.maak_relatie(gebruiker_id, taak_id)

def test_maak_relatie_ongeldige_gebruiker():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 9999  # bestaat niet!
    taak_id = 22
    with pytest.raises(OngeldigeGebruikerException):
        service.maak_relatie(gebruiker_id, taak_id)

def test_maak_relatie_ongeldige_taak():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 15
    taak_id = 9999  # bestaat niet!
    with pytest.raises(OngeldigeVernietigingstaakException):
        service.maak_relatie(gebruiker_id, taak_id)

def test_verwijder_relatie_succesvol():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 30
    taak_id = 40
    service.opslaan_relatie(gebruiker_id, taak_id)
    assert service.bestaat_relatie(gebruiker_id, taak_id)
    service.verwijder_relatie(gebruiker_id, taak_id)
    assert not service.bestaat_relatie(gebruiker_id, taak_id)

def test_verwijder_relatie_niet_gevonden():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 31
    taak_id = 41
    assert not service.bestaat_relatie(gebruiker_id, taak_id)
    with pytest.raises(VTBehandelaarRelatieNietGevondenException):
        service.verwijder_relatie(gebruiker_id, taak_id)

def test_haal_relaties_op_succesvol():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 50
    taak_id1 = 60
    taak_id2 = 61
    service.opslaan_relatie(gebruiker_id, taak_id1)
    service.opslaan_relatie(gebruiker_id, taak_id2)
    relaties = service.haal_relaties_op(gebruiker_id)
    assert {'gebruiker_id': gebruiker_id, 'taak_id': taak_id1} in relaties
    assert {'gebruiker_id': gebruiker_id, 'taak_id': taak_id2} in relaties
    assert len(relaties) == 2

def test_haal_relaties_op_ongeldige_gebruiker():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 8888 # bestaat niet
    with pytest.raises(OngeldigeGebruikerException):
        service.haal_relaties_op(gebruiker_id)
