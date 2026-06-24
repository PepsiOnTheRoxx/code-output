import pytest
from src.readvernietigingstaak import DestructionTaskService, VernietigingstaakNotFound, Vernietigingstaak

@pytest.fixture
def service_with_data():
    service = DestructionTaskService()
    task1 = Vernietigingstaak(id=1, description="Vernietig archief X")
    task2 = Vernietigingstaak(id=2, description="Vernietig archief Y")
    service._tasks = {1: task1, 2: task2}
    return service

def test_read_existing_vernietigingstaak(service_with_data):
    result = service_with_data.read(1)
    assert isinstance(result, Vernietigingstaak)
    assert result.id == 1
    assert result.description == "Vernietig archief X"

def test_read_another_existing_vernietigingstaak(service_with_data):
    result = service_with_data.read(2)
    assert isinstance(result, Vernietigingstaak)
    assert result.id == 2
    assert result.description == "Vernietig archief Y"

def test_read_non_existing_vernietigingstaak_raises(service_with_data):
    with pytest.raises(VernietigingstaakNotFound):
        service_with_data.read(999)

def test_read_with_invalid_id_type(service_with_data):
    with pytest.raises(TypeError):
        service_with_data.read("invalid")

def test_read_empty_repository():
    service = DestructionTaskService()
    with pytest.raises(VernietigingstaakNotFound):
        service.read(1)