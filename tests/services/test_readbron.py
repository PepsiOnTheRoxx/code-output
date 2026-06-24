import pytest
from unittest.mock import patch, MagicMock
from src.services.readbron import BronService, BronRepository
from src.services.readbron_exceptions import BronNotFoundException, BronReadException

def test_read_bron_returns_bron_object():
    bron_repo = BronRepository()
    dummy_bron = {"id": 12, "naam": "TestBron"}
    service = BronService()
    # Geen mock nodig, want Repository is nu geimplementeerd
    bron = service.read_bron(12)
    assert bron == dummy_bron

def test_read_bron_raises_not_found_exception():
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.read_bron(9999)

def test_read_bron_handles_repository_errors():
    with patch("src.services.readbron.BronRepository.get_bron_by_id", side_effect=Exception("Database error")) as mock_method:
        service = BronService()
        with pytest.raises(BronReadException):
            service.read_bron(12)
        mock_method.assert_called_once_with(12)

def test_read_bron_with_invalid_id_type():
    service = BronService()
    with pytest.raises(TypeError):
        service.read_bron("ongeldig_id")
