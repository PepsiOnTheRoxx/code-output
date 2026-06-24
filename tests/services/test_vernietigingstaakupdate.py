import pytest
from src.services.vernietigingstaakupdate import VernietigingstaakService
from src.services.vernietigingstaakupdate_exceptions import VernietigingstaakNotFoundException, InvalidVernietigingstaakUpdateException

@pytest.fixture
def bestaande_taak():
    return {
        "id": 1,
        "naam": "Taak 001",
        "status": "Open",
        "omschrijving": "Eerste vernietigingstaak"
    }

@pytest.fixture
def service(mocker, bestaande_taak):
    mock = mocker.patch("src.services.vernietigingstaakupdate.VernietigingstaakRepository")
    repo_instance = mock.return_value
    repo_instance.get_by_id.return_value = bestaande_taak.copy()
    return VernietigingstaakService(repo_instance)

def test_update_bestaande_taak_succesvol(service, bestaande_taak):
    update_data = {
        "id": bestaande_taak["id"],
        "naam": "Gewijzigde taak",
        "omschrijving": "Aangepaste omschrijving"
    }
    result = service.update_vernietigingstaak(update_data)
    assert result["naam"] == "Gewijzigde taak"
    assert result["omschrijving"] == "Aangepaste omschrijving"
    assert result["id"] == bestaande_taak["id"]

def test_update_naar_bestaande_status(service, bestaande_taak):
    update_data = {
        "id": bestaande_taak["id"],
        "status": "Voltooid"
    }
    result = service.update_vernietigingstaak(update_data)
    assert result["status"] == "Voltooid"

def test_update_vernietigingstaak_bestaat_niet(mocker):
    mock = mocker.patch("src.services.vernietigingstaakupdate.VernietigingstaakRepository")
    repo_instance = mock.return_value
    repo_instance.get_by_id.return_value = None
    service = VernietigingstaakService(repo_instance)
    update_data = {
        "id": 999,
        "naam": "Onbekende taak"
    }
    with pytest.raises(VernietigingstaakNotFoundException):
        service.update_vernietigingstaak(update_data)

def test_update_vernietigingstaak_ongeldige_input(service):
    update_data = {
        "id": None,
        "naam": ""
    }
    with pytest.raises(InvalidVernietigingstaakUpdateException):
        service.update_vernietigingstaak(update_data)

def test_update_vernietigingstaak_deeltijd_update(service, bestaande_taak):
    update_data = {
        "id": bestaande_taak["id"],
        "omschrijving": "Alleen omschrijving gewijzigd"
    }
    result = service.update_vernietigingstaak(update_data)
    assert result["omschrijving"] == "Alleen omschrijving gewijzigd"
    assert result["naam"] == bestaande_taak["naam"]

def test_update_vernietigingstaak_bewaart_restant(service, bestaande_taak):
    update_data = {
        "id": bestaande_taak["id"],
        "status": "InBehandeling"
    }
    result = service.update_vernietigingstaak(update_data)
    assert result["id"] == bestaande_taak["id"]
    assert result["status"] == "InBehandeling"
    assert result["naam"] == bestaande_taak["naam"]
    assert result["omschrijving"] == bestaande_taak["omschrijving"]