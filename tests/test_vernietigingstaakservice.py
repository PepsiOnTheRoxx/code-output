import pytest
from src.vernietigingstaakservice import VernietigingstaakService, Vernietigingstaak

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_create_vernietigingstaak_success(service):
    aantekeningen = "Dit is een test taak"
    datum = "2024-06-12"
    status = "In behandeling"
    task = service.create_vernietigingstaak(aantekeningen, datum, status)
    assert isinstance(task, Vernietigingstaak)
    assert task.aantekeningen == aantekeningen
    assert task.datum == datum
    assert task.status == status

def test_create_vernietigingstaak_missing_aantekeningen(service):
    datum = "2024-06-12"
    status = "In behandeling"
    with pytest.raises(ValueError):
        service.create_vernietigingstaak(None, datum, status)

def test_create_vernietigingstaak_invalid_datum(service):
    aantekeningen = "Vernietiging gepland"
    datum = "invalid-date"
    status = "Gepland"
    with pytest.raises(ValueError):
        service.create_vernietigingstaak(aantekeningen, datum, status)

def test_create_vernietigingstaak_invalid_status(service):
    aantekeningen = "Test"
    datum = "2024-06-12"
    status = "Onbekend"
    with pytest.raises(ValueError):
        service.create_vernietigingstaak(aantekeningen, datum, status)

def test_create_vernietigingstaak_persists_task(service):
    aantekeningen = "Bewaar termijn is verstreken"
    datum = "2024-06-13"
    status = "Voltooid"
    task = service.create_vernietigingstaak(aantekeningen, datum, status)
    assert task in service.tasks