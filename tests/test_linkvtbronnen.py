import pytest
from src.linkvtbronnen import VernietigingstaakRelatiesService
from src.linkvtbronnen_exceptions import BronNotFoundException, VernietigingstaakNotFoundException, BronAlGekoppeldException

@pytest.fixture
def service():
    return VernietigingstaakRelatiesService()

@pytest.fixture
def bron_id():
    return "BRON123"

@pytest.fixture
def vernietigingstaak_id():
    return "VT456"

def test_link_bron_succes(service, bron_id, vernietigingstaak_id):
    service.add_bron(bron_id)
    service.add_vernietigingstaak(vernietigingstaak_id)
    service.link_bron_aan_vernietigingstaak(bron_id, vernietigingstaak_id)
    assert service.is_bron_gekoppeld_aan_vernietigingstaak(bron_id, vernietigingstaak_id) is True

def test_link_bron_aan_onbestaande_bron(service, vernietigingstaak_id):
    service.add_vernietigingstaak(vernietigingstaak_id)
    with pytest.raises(BronNotFoundException):
        service.link_bron_aan_vernietigingstaak("ONBEKENDE_BRON", vernietigingstaak_id)

def test_link_bron_aan_onbestaande_vernietigingstaak(service, bron_id):
    service.add_bron(bron_id)
    with pytest.raises(VernietigingstaakNotFoundException):
        service.link_bron_aan_vernietigingstaak(bron_id, "ONBEKEND_VT")

def test_bron_meermaals_koppelen(service, bron_id, vernietigingstaak_id):
    service.add_bron(bron_id)
    service.add_vernietigingstaak(vernietigingstaak_id)
    service.link_bron_aan_vernietigingstaak(bron_id, vernietigingstaak_id)
    with pytest.raises(BronAlGekoppeldException):
        service.link_bron_aan_vernietigingstaak(bron_id, vernietigingstaak_id)

def test_meerdere_bronden_aan_vernietigingstaak(service, vernietigingstaak_id):
    bron1 = "BRON_1"
    bron2 = "BRON_2"
    service.add_bron(bron1)
    service.add_bron(bron2)
    service.add_vernietigingstaak(vernietigingstaak_id)
    service.link_bron_aan_vernietigingstaak(bron1, vernietigingstaak_id)
    service.link_bron_aan_vernietigingstaak(bron2, vernietigingstaak_id)
    assert service.is_bron_gekoppeld_aan_vernietigingstaak(bron1, vernietigingstaak_id) is True
    assert service.is_bron_gekoppeld_aan_vernietigingstaak(bron2, vernietigingstaak_id) is True

def test_koppel_bron_aan_meerdere_vernietigingstaken(service, bron_id):
    vt1 = "VT1"
    vt2 = "VT2"
    service.add_bron(bron_id)
    service.add_vernietigingstaak(vt1)
    service.add_vernietigingstaak(vt2)
    service.link_bron_aan_vernietigingstaak(bron_id, vt1)
    service.link_bron_aan_vernietigingstaak(bron_id, vt2)
    assert service.is_bron_gekoppeld_aan_vernietigingstaak(bron_id, vt1) is True
    assert service.is_bron_gekoppeld_aan_vernietigingstaak(bron_id, vt2) is True