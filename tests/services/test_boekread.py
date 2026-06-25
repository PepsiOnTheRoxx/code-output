import pytest
from unittest.mock import patch, MagicMock
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNotFoundException

@pytest.fixture
def mock_boek_list():
    return [
        {"id": 1, "titel": "Boek A", "auteur": "Auteur A"},
        {"id": 2, "titel": "Boek B", "auteur": "Auteur B"},
    ]

def test_get_all_boeken_returns_list_of_boeken(mock_boek_list):
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_all_boeken.return_value = mock_boek_list
        service = BoekService()
        result = service.get_all_boeken()
        assert result == mock_boek_list
        instance.get_all_boeken.assert_called_once()

def test_get_boek_by_id_returns_correct_boek(mock_boek_list):
    boek_id = 1
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_boek_by_id.return_value = mock_boek_list[0]
        service = BoekService()
        result = service.get_boek_by_id(boek_id)
        assert result == mock_boek_list[0]
        instance.get_boek_by_id.assert_called_once_with(boek_id)

def test_get_boek_by_id_raises_not_found_exception():
    boek_id = 99
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_boek_by_id.return_value = None
        service = BoekService()
        with pytest.raises(BoekNotFoundException):
            service.get_boek_by_id(boek_id)
        instance.get_boek_by_id.assert_called_once_with(boek_id)

def test_get_all_boeken_empty_list():
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_all_boeken.return_value = []
        service = BoekService()
        result = service.get_all_boeken()
        assert result == []
        instance.get_all_boeken.assert_called_once()

def test_get_boek_by_id_invalid_type():
    boek_id = "invalid"
    with patch('src.services.boekread.BoekRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_boek_by_id.side_effect = TypeError()
        service = BoekService()
        with pytest.raises(TypeError):
            service.get_boek_by_id(boek_id)
        instance.get_boek_by_id.assert_called_once_with(boek_id)
