import pytest
from unittest.mock import patch, MagicMock
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNotFoundException, InvalidBoekIdException

def test_read_boek_returns_boek_object():
    mock_boek = {"id": 1, "titel": "Test Boek", "auteur": "Auteur Naam"}
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = mock_boek
        service = BoekService()
        result = service.read_boek(1)
        assert result == mock_boek
        instance.get_by_id.assert_called_once_with(1)

def test_read_boek_raises_not_found_when_boek_missing():
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = None
        service = BoekService()
        with pytest.raises(BoekNotFoundException):
            service.read_boek(999)

def test_read_boek_raises_invalid_input_for_none_id():
    service = BoekService()
    with pytest.raises(InvalidBoekIdException):
        service.read_boek(None)

def test_read_boek_repository_called_with_correct_id():
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = {"id": 5, "titel": "Boek 5"}
        service = BoekService()
        service.read_boek(5)
        instance.get_by_id.assert_called_with(5)

def test_read_boek_raises_invalid_input_for_negative_id():
    service = BoekService()
    with pytest.raises(InvalidBoekIdException):
        service.read_boek(-2)