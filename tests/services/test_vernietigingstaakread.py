import pytest
from src.services.vernietigingstaakread import VernietigingstaakService
from src.services.vernietigingstaakread_exceptions import VernietigingstaakNotFoundError, VernietigingstaakPermissionDeniedError

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_read_existing_vernietigingstaak_returns_correct_data(service):
    vernietigingstaak_id = 42
    expected_data = {
        "id": vernietigingstaak_id,
        "status": "aangemaakt",
        "omschrijving": "Test vernietiging",
        "object_type": 10
    }
    result = service.read(vernietigingstaak_id)
    assert result == expected_data
    assert result["object_type"] == 10

def test_read_nonexistent_vernietigingstaak_raises_not_found(service):
    vernietigingstaak_id = 999
    with pytest.raises(VernietigingstaakNotFoundError):
        service.read(vernietigingstaak_id)

def test_read_vernietigingstaak_unauthorized_access_raises_exception(service):
    vernietigingstaak_id = 7
    with pytest.raises(VernietigingstaakPermissionDeniedError):
        service.read(vernietigingstaak_id)

def test_read_existing_vernietigingstaak_contains_expected_keys(service):
    vernietigingstaak_id = 55
    result = service.read(vernietigingstaak_id)
    assert "id" in result
    assert "status" in result
    assert "omschrijving" in result
    assert "object_type" in result

def test_read_existing_vernietigingstaak_with_different_status(service):
    vernietigingstaak_id = 123
    result = service.read(vernietigingstaak_id)
    assert result["status"] == "in_behandeling"
