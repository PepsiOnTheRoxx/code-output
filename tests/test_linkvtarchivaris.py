import pytest
from src.linkvtarchivaris import VernietigingstaakRelatiesService
from src.linkvtarchivaris_exceptions import ArchivarisNotFoundException, ArchivarisAlreadyLinkedException, VernietigingstaakNotFoundException, InvalidArchivarisRoleException

@pytest.fixture
def service():
    return VernietigingstaakRelatiesService()

def test_link_geverifieerde_gebruiker_als_archivaris_succesvol(service):
    gebruiker_id = 100
    taak_id = 200
    # Zorg voor een gebruiker en vernietigingstaak in de test-setup van het service object
    result = service.link_archivaris_aan_vernietigingstaak(gebruiker_id, taak_id)
    assert result is True
    assert service.is_archivaris_gekopppeld(gebruiker_id, taak_id) is True

def test_gebruiker_niet_gevonden(service):
    gebruiker_id = 9999  # aannemen dat deze niet bestaat
    taak_id = 200
    with pytest.raises(ArchivarisNotFoundException):
        service.link_archivaris_aan_vernietigingstaak(gebruiker_id, taak_id)

def test_vernietigingstaak_niet_gevonden(service):
    gebruiker_id = 100
    taak_id = 8888  # aannemen dat deze niet bestaat
    with pytest.raises(VernietigingstaakNotFoundException):
        service.link_archivaris_aan_vernietigingstaak(gebruiker_id, taak_id)

def test_archivaris_al_gekoppeld(service):
    gebruiker_id = 110
    taak_id = 220
    service.link_archivaris_aan_vernietigingstaak(gebruiker_id, taak_id)
    with pytest.raises(ArchivarisAlreadyLinkedException):
        service.link_archivaris_aan_vernietigingstaak(gebruiker_id, taak_id)

def test_onvoldoende_rechten_gebruiker(service):
    gebruiker_id = 120  # gebruiker zonder juiste permissie
    taak_id = 230
    # Stel permissie in dat gebruiker geen archivaris mag worden
    service.set_rechten(gebruiker_id, allowed=False)
    with pytest.raises(InvalidArchivarisRoleException):
        service.link_archivaris_aan_vernietigingstaak(gebruiker_id, taak_id)
