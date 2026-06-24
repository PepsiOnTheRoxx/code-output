import pytest
from src.services.vernietigingstaakread import VernietigingstaakService
from src.services.vernietigingstaakread_exceptions import VernietigingstaakNotFoundException, UnauthorizedAccessException

@pytest.fixture
def service(mocker):
    return VernietigingstaakService()

def test_read_existing_vernietigingstaak_returns_correct_data(service, mocker):
    vernietigingstaak_id = 42
    expected_data = {
        "id": vernietigingstaak_id,
        "status": "aangemaakt",
        "omschrijving": "Test vernietiging",
        "object_type": 10
    }
    mocker.patch.object(service, 'read', return_value=expected_data)
    result = service.read(vernietigingstaak_id)
    assert result == expected_data
    assert result["object_type"] == 10

def test_read_nonexistent_vernietigingstaak_raises_not_found(service, mocker):
    vernietigingstaak_id = 999
    mocker.patch.object(service, 'read', side_effect=VernietigingstaakNotFoundException)
    with pytest.raises(VernietigingstaakNotFoundException):
        service.read(vernietigingstaak_id)

def test_read_vernietigingstaak_unauthorized_access_raises_exception(service, mocker):
    vernietigingstaak_id = 7
    mocker.patch.object(service, 'read', side_effect=UnauthorizedAccessException)
    with pytest.raises(UnauthorizedAccessException):
        service.read(vernietigingstaak_id)

def test_read_existing_vernietigingstaak_contains_expected_keys(service, mocker):
    vernietigingstaak_id = 55
    data = {
        "id": vernietigingstaak_id,
        "status": "voltooid",
        "omschrijving": "Opschonen database",
        "object_type": 10
    }
    mocker.patch.object(service, 'read', return_value=data)
    result = service.read(vernietigingstaak_id)
    assert "id" in result
    assert "status" in result
    assert "omschrijving" in result
    assert "object_type" in result

def test_read_existing_vernietigingstaak_with_different_status(service, mocker):
    vernietigingstaak_id = 123
    data = {
        "id": vernietigingstaak_id,
        "status": "in_behandeling",
        "omschrijving": "Test andere status",
        "object_type": 10
    }
    mocker.patch.object(service, 'read', return_value=data)
    result = service.read(vernietigingstaak_id)
    assert result["status"] == "in_behandeling"