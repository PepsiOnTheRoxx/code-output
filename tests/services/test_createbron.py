from src.services.createbron import BronService
from src.services.createbron_exceptions import BronAlreadyExistsException, InvalidBronDataException
import pytest
from unittest.mock import patch, MagicMock


def test_create_bron_success():
    service = BronService()
    naam = "TestBron"
    beschrijving = "Een beschrijving"
    bron_mock = MagicMock()
    with patch.object(service, 'bron_repository') as mock_repo:
        mock_repo.exists.return_value = False
        mock_repo.create.return_value = bron_mock
        result = service.create_bron(naam, beschrijving)
        mock_repo.exists.assert_called_once_with(naam)
        mock_repo.create.assert_called_once_with(naam, beschrijving)
        assert result == bron_mock

def test_create_bron_already_exists():
    service = BronService()
    naam = "DubbelBron"
    beschrijving = "Al bestaand"
    with patch.object(service, 'bron_repository') as mock_repo:
        mock_repo.exists.return_value = True
        with pytest.raises(BronAlreadyExistsException):
            service.create_bron(naam, beschrijving)
        mock_repo.exists.assert_called_once_with(naam)
        mock_repo.create.assert_not_called()

def test_create_bron_invalid_data():
    service = BronService()
    with patch.object(service, 'bron_repository') as mock_repo:
        # Lege naam
        with pytest.raises(InvalidBronDataException):
            service.create_bron("", "Beschrijving")
        # Geen beschrijving
        with pytest.raises(InvalidBronDataException):
            service.create_bron("BronZonderBeschrijving", "")
        mock_repo.create.assert_not_called()
        mock_repo.exists.assert_not_called()

def test_create_bron_handles_repository_exception():
    service = BronService()
    naam = "CrashBron"
    beschrijving = "Dit veroorzaakt een crash"
    with patch.object(service, 'bron_repository') as mock_repo:
        mock_repo.exists.return_value = False
        mock_repo.create.side_effect = Exception("Database error")
        with pytest.raises(Exception) as excinfo:
            service.create_bron(naam, beschrijving)
        assert "Database error" in str(excinfo.value)
        mock_repo.exists.assert_called_once_with(naam)
        mock_repo.create.assert_called_once_with(naam, beschrijving)