import pytest
from unittest.mock import patch, MagicMock
from src.services.readbron import BronService
from src.services.readbron_exceptions import BronNotFoundException, BronReadException

def test_read_bron_returns_bron_object():
    dummy_bron = {"id": 12, "naam": "TestBron"}
    with patch("src.services.readbron.BronRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_bron_by_id.return_value = dummy_bron
        service = BronService()
        bron = service.read_bron(12)
        assert bron == dummy_bron
        instance.get_bron_by_id.assert_called_once_with(12)

def test_read_bron_raises_not_found_exception():
    with patch("src.services.readbron.BronRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_bron_by_id.return_value = None
        service = BronService()
        with pytest.raises(BronNotFoundException):
            service.read_bron(9999)
        instance.get_bron_by_id.assert_called_once_with(9999)

def test_read_bron_handles_repository_errors():
    with patch("src.services.readbron.BronRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_bron_by_id.side_effect = Exception("Database error")
        service = BronService()
        with pytest.raises(BronReadException):
            service.read_bron(12)
        instance.get_bron_by_id.assert_called_once_with(12)

def test_read_bron_with_invalid_id_type():
    service = BronService()
    with pytest.raises(TypeError):
        service.read_bron("ongeldig_id")
