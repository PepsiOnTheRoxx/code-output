import pytest
from datetime import datetime
from src.readvernietigingstaak import VernietigingstaakService
from src.readvernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    UnauthorizedAccessException,
)

@pytest.fixture
def mock_task():
    return {
        "id": 1,
        "aantekeningen": "Let op asbest!",
        "datum": datetime(2024, 6, 13, 10, 30),
        "status": "INGEPLAND"
    }

@pytest.fixture
def service_with_task(mock_task, monkeypatch):
    service = VernietigingstaakService()
    monkeypatch.setattr(service, "get_vernietigingstaak_by_id", lambda taak_id: mock_task)
    return service

def test_read_vernietigingstaak_returns_correct_data(service_with_task, mock_task):
    result = service_with_task.read_vernietigingstaak(1)
    assert result["id"] == mock_task["id"]
    assert result["aantekeningen"] == mock_task["aantekeningen"]
    assert result["datum"] == mock_task["datum"]
    assert result["status"] == mock_task["status"]

def test_read_vernietigingstaak_handles_nonexistent_id(monkeypatch):
    service = VernietigingstaakService()
    def raise_not_found(_):
        raise VernietigingstaakNotFoundException()
    monkeypatch.setattr(service, "get_vernietigingstaak_by_id", raise_not_found)
    with pytest.raises(VernietigingstaakNotFoundException):
        service.read_vernietigingstaak(999)

def test_read_vernietigingstaak_unauthorized_access(monkeypatch):
    service = VernietigingstaakService()
    def raise_unauthorized(_):
        raise UnauthorizedAccessException()
    monkeypatch.setattr(service, "get_vernietigingstaak_by_id", raise_unauthorized)
    with pytest.raises(UnauthorizedAccessException):
        service.read_vernietigingstaak(2)

def test_read_vernietigingstaak_contains_required_fields(service_with_task):
    result = service_with_task.read_vernietigingstaak(1)
    assert "id" in result
    assert "aantekeningen" in result
    assert "datum" in result
    assert "status" in result

def test_read_vernietigingstaak_status_is_valid(service_with_task):
    result = service_with_task.read_vernietigingstaak(1)
    assert result["status"] in ["INGEPLAND", "UITGEVOERD", "GEANNULEERD"]
