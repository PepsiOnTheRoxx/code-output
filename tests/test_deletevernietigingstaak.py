import pytest
from src.deletevernietigingstaak import DestructionTaskService, VernietigingstaakNotFound, Vernietigingstaak

@pytest.fixture
def sample_vernietigingstaken():
    return [
        Vernietigingstaak(id=1, naam="Taak A"),
        Vernietigingstaak(id=2, naam="Taak B"),
        Vernietigingstaak(id=3, naam="Taak C"),
    ]

@pytest.fixture
def service(sample_vernietigingstaken):
    return DestructionTaskService(vernietigingstaken=list(sample_vernietigingstaken))

def test_delete_existing_vernietigingstaak(service):
    service.delete_vernietigingstaak(2)
    ids = [t.id for t in service.vernietigingstaken]
    assert 2 not in ids
    assert len(service.vernietigingstaken) == 2

def test_delete_non_existing_vernietigingstaak_raises_exception(service):
    with pytest.raises(VernietigingstaakNotFound):
        service.delete_vernietigingstaak(99)

def test_delete_all_vernietigingstaken_one_by_one(service):
    ids_to_delete = [t.id for t in service.vernietigingstaken]
    for id_ in ids_to_delete:
        service.delete_vernietigingstaak(id_)
    assert service.vernietigingstaken == []

def test_delete_vernietigingstaak_removes_correct_object(service):
    initial_names = [t.naam for t in service.vernietigingstaken]
    assert "Taak B" in initial_names
    service.delete_vernietigingstaak(2)
    remaining_names = [t.naam for t in service.vernietigingstaken]
    assert "Taak B" not in remaining_names
    assert set(remaining_names) == {"Taak A", "Taak C"}

def test_delete_vernietigingstaak_invalid_id(service):
    # Negative id
    with pytest.raises(VernietigingstaakNotFound):
        service.delete_vernietigingstaak(-1)
    # None as id
    with pytest.raises(VernietigingstaakNotFound):
        service.delete_vernietigingstaak(None)
    # String id
    with pytest.raises(VernietigingstaakNotFound):
        service.delete_vernietigingstaak("invalid")

def test_delete_vernietigingstaak_twice_raises_exception(service):
    service.delete_vernietigingstaak(1)
    with pytest.raises(VernietigingstaakNotFound):
        service.delete_vernietigingstaak(1)