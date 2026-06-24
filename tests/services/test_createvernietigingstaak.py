import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.services.createvernietigingstaak import VernietigingstaakService
from src.services.createvernietigingstaak_exceptions import InvalidStatusException, MissingAttributeException

@pytest.fixture
def vernietigingstaak_data():
    return {
        "aantekeningen": "Test aantekeningen",
        "datum": datetime(2024, 5, 10),
        "status": "GEPLAND"
    }

def test_create_vernietigingstaak_success(vernietigingstaak_data):
    with patch("src.services.createvernietigingstaak.VernietigingstaakRepository") as MockRepo:
        repo_instance = MockRepo.return_value
        repo_instance.create.return_value = MagicMock(**vernietigingstaak_data)
        service = VernietigingstaakService()
        taak = service.create_vernietigingstaak(
            aantekeningen=vernietigingstaak_data["aantekeningen"],
            datum=vernietigingstaak_data["datum"],
            status=vernietigingstaak_data["status"]
        )
        assert taak.aantekeningen == vernietigingstaak_data["aantekeningen"]
        assert taak.datum == vernietigingstaak_data["datum"]
        assert taak.status == vernietigingstaak_data["status"]

@pytest.mark.parametrize("status", ["ONGELDIG", "", None])
def test_create_vernietigingstaak_invalid_status(vernietigingstaak_data, status):
    with patch("src.services.createvernietigingstaak.VernietigingstaakRepository"):
        service = VernietigingstaakService()
        with pytest.raises(InvalidStatusException):
            service.create_vernietigingstaak(
                aantekeningen=vernietigingstaak_data["aantekeningen"],
                datum=vernietigingstaak_data["datum"],
                status=status
            )

@pytest.mark.parametrize("missing_field", ["aantekeningen", "datum", "status"])
def test_create_vernietigingstaak_missing_required_attribute(vernietigingstaak_data, missing_field):
    with patch("src.services.createvernietigingstaak.VernietigingstaakRepository"):
        data = dict(vernietigingstaak_data)
        data.pop(missing_field)
        service = VernietigingstaakService()
        with pytest.raises(MissingAttributeException):
            service.create_vernietigingstaak(**data)