import pytest
from unittest.mock import patch, MagicMock
from src.services.readgebruiker import GebruikerService
from src.services.readgebruiker_exceptions import GebruikerNotFoundException, InvalidGebruikerIdException

def test_read_gebruiker_returns_gebruiker_dict():
    gebruiker_id = 123
    expected_gebruiker = {
        "id": gebruiker_id,
        "naam": "Jan Jansen",
        "email": "jan.jansen@example.com",
        "active": True
    }
    with patch('src.services.readgebruiker.GebruikerRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.get_gebruiker_by_id.return_value = expected_gebruiker
        service = GebruikerService()
        result = service.read_gebruiker(gebruiker_id)
        assert result == expected_gebruiker
        mock_repo.get_gebruiker_by_id.assert_called_once_with(gebruiker_id)

def test_read_gebruiker_raises_gebuiker_not_found():
    gebruiker_id = 555
    with patch('src.services.readgebruiker.GebruikerRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.get_gebruiker_by_id.side_effect = GebruikerNotFoundException("Not found")
        service = GebruikerService()
        with pytest.raises(GebruikerNotFoundException):
            service.read_gebruiker(gebruiker_id)
        mock_repo.get_gebruiker_by_id.assert_called_once_with(gebruiker_id)

def test_read_gebruiker_raises_invalid_id():
    invalid_id = "abc"
    service = GebruikerService()
    with pytest.raises(InvalidGebruikerIdException):
        service.read_gebruiker(invalid_id)
        
def test_read_gebruiker_passes_through_other_exceptions():
    gebruiker_id = 42
    with patch('src.services.readgebruiker.GebruikerRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.get_gebruiker_by_id.side_effect = RuntimeError("Database down")
        service = GebruikerService()
        with pytest.raises(RuntimeError):
            service.read_gebruiker(gebruiker_id)
        mock_repo.get_gebruiker_by_id.assert_called_once_with(gebruiker_id)