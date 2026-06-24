import pytest
from src.vernietigingstaakservice import VernietigingstaakService

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_read_vernietigingstaak_returns_expected_object(service):
    taak_id = 1
    result = service.read_vernietigingstaak(taak_id)
    assert isinstance(result, dict)
    assert "id" in result
    assert result["id"] == taak_id

def test_read_vernietigingstaak_includes_all_attributes(service):
    taak_id = 2
    result = service.read_vernietigingstaak(taak_id)
    assert "id" in result
    assert "status" in result
    assert "datum" in result

def test_read_vernietigingstaak_invalid_id_returns_none_or_raises(service):
    invalid_id = 9999
    with pytest.raises(Exception) or service.read_vernietigingstaak(invalid_id) is None:
        service.read_vernietigingstaak(invalid_id)

def test_read_vernietigingstaak_multiple_calls_consistent(service):
    taak_id = 3
    result1 = service.read_vernietigingstaak(taak_id)
    result2 = service.read_vernietigingstaak(taak_id)
    assert result1 == result2

def test_read_vernietigingstaak_attributes_types(service):
    taak_id = 4
    result = service.read_vernietigingstaak(taak_id)
    assert isinstance(result["id"], int)
    assert isinstance(result["status"], str)
    assert isinstance(result["datum"], str)