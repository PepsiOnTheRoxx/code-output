import pytest
from unittest.mock import patch, MagicMock
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNotFoundException, InvalidBoekDataException

@pytest.fixture
def valid_boek_data():
    return {
        "id": 1,
        "titel": "Nieuwe Titel",
        "auteur": "Nieuwe Auteur",
        "jaar": 2023,
        "isbn": "9780123456789"
    }

def test_update_boek_success(valid_boek_data):
    with patch("src.services.boekupdate.BoekRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_boek_by_id.return_value = MagicMock()
        mock_repo.update_boek.return_value = True
        mock_repo_class.return_value = mock_repo
        service = BoekService()
        result = service.update_boek(valid_boek_data["id"], valid_boek_data)
        assert result is True
        mock_repo.get_boek_by_id.assert_called_once_with(valid_boek_data["id"])
        mock_repo.update_boek.assert_called_once()

def test_update_boek_not_found(valid_boek_data):
    with patch("src.services.boekupdate.BoekRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_boek_by_id.return_value = None
        mock_repo_class.return_value = mock_repo
        service = BoekService()
        with pytest.raises(BoekNotFoundException):
            service.update_boek(valid_boek_data["id"], valid_boek_data)
        mock_repo.get_boek_by_id.assert_called_once_with(valid_boek_data["id"])
        mock_repo.update_boek.assert_not_called()

def test_update_boek_invalid_data():
    invalid_data = {
        "id": 2,
        "titel": "",
        "auteur": "Auteur",
        "jaar": 2023,
        "isbn": "123"  # Ongeldig ISBN
    }
    with patch("src.services.boekupdate.BoekRepository"):
        service = BoekService()
        with pytest.raises(InvalidBoekDataException):
            service.update_boek(invalid_data["id"], invalid_data)

def test_update_boek_update_fails(valid_boek_data):
    with patch("src.services.boekupdate.BoekRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_boek_by_id.return_value = MagicMock()
        mock_repo.update_boek.return_value = False
        mock_repo_class.return_value = mock_repo
        service = BoekService()
        result = service.update_boek(valid_boek_data["id"], valid_boek_data)
        assert result is False
        mock_repo.get_boek_by_id.assert_called_once_with(valid_boek_data["id"])
        mock_repo.update_boek.assert_called_once()

def test_update_boek_database_exception(valid_boek_data):
    with patch("src.services.boekupdate.BoekRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_boek_by_id.return_value = MagicMock()
        mock_repo.update_boek.side_effect = Exception("Database error")
        mock_repo_class.return_value = mock_repo
        service = BoekService()
        with pytest.raises(Exception) as excinfo:
            service.update_boek(valid_boek_data["id"], valid_boek_data)
        assert "Database error" in str(excinfo.value)
        mock_repo.get_boek_by_id.assert_called_once_with(valid_boek_data["id"])
        mock_repo.update_boek.assert_called_once()
