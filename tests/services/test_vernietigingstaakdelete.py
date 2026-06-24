import pytest
from src.services.vernietigingstaakdelete import VernietigingstaakService
from src.services.vernietigingstaakdelete_exceptions import VernietigingstaakNotFoundException, VernietigingstaakDeleteException

@pytest.fixture
def vernietigingstaak_service():
    service = VernietigingstaakService()
    # Voeg een test taak toe
    service._vernietigingstaken[123] = "dummy"
    service._vernietigingstaken[789] = "dummy2"
    service._vernietigingstaken[456] = "dummy3"
    return service

def test_delete_bestaande_vernietigingstaak_succesvol_verwijderd(vernietigingstaak_service):
    resultaat = vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=123)
    assert resultaat is True
    assert 123 not in vernietigingstaak_service._vernietigingstaken

def test_delete_niet_bestaande_vernietigingstaak_raised_not_found(vernietigingstaak_service):
    with pytest.raises(VernietigingstaakNotFoundException, match="Taak bestaat niet"):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=999)

def test_delete_vernietigingstaak_onverwachte_fout_raised_delete_error(monkeypatch, vernietigingstaak_service):
    def faulty_del(taak_id):
        raise Exception("storage kapot")
    monkeypatch.setattr(vernietigingstaak_service, "_del_vernietigingstaak", faulty_del)
    with pytest.raises(VernietigingstaakDeleteException, match="Verwijderen mislukt"):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=456)

def test_delete_vernietigingstaak_meerdere_keers_geen_extra_verwijdering(vernietigingstaak_service):
    vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=789)
    with pytest.raises(VernietigingstaakNotFoundException):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=789)

def test_delete_vernietigingstaak_invalid_argument_type(vernietigingstaak_service):
    with pytest.raises(TypeError):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=None)
    with pytest.raises(TypeError):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id="abc")
