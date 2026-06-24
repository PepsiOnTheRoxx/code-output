import pytest
from unittest.mock import patch, MagicMock
from src.services.bronread import BronService
from src.services.bronread_exceptions import BronNotFoundException, BronAccessException

def test_get_bron_by_id_returns_bron_object():
    bron_id = 1
    expected_bron = {'id': bron_id, 'naam': "TestBron"}
    with patch("src.services.bronread.BronRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id.return_value = expected_bron
        service = BronService()
        result = service.get_bron_by_id(bron_id)
        assert result == expected_bron
        mock_repo_instance.get_by_id.assert_called_once_with(bron_id)

def test_get_bron_by_id_not_found_raises_exception():
    bron_id = 99
    with patch("src.services.bronread.BronRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id.return_value = None
        service = BronService()
        with pytest.raises(BronNotFoundException):
            service.get_bron_by_id(bron_id)

def test_get_all_bronnen_returns_list_of_bronnen():
    expected_bronnen = [
        {'id': 1, 'naam': 'BronA'},
        {'id': 2, 'naam': 'BronB'}
    ]
    with patch("src.services.bronread.BronRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_all.return_value = expected_bronnen
        service = BronService()
        result = service.get_all_bronnen()
        assert result == expected_bronnen
        mock_repo_instance.get_all.assert_called_once()

def test_get_bron_by_id_raises_access_exception_on_permission_denied():
    bron_id = 2
    with patch("src.services.bronread.BronRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id.side_effect = BronAccessException("Geen toegang tot bron")
        service = BronService()
        with pytest.raises(BronAccessException):
            service.get_bron_by_id(bron_id)

def test_get_all_bronnen_empty_list():
    with patch("src.services.bronread.BronRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_all.return_value = []
        service = BronService()
        result = service.get_all_bronnen()
        assert result == []
        mock_repo_instance.get_all.assert_called_once()

def test_get_bron_by_id_calls_repository_once():
    bron_id = 3
    bron_obj = {'id': bron_id, 'naam': "BronX"}
    with patch("src.services.bronread.BronRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = bron_obj
        service = BronService()
        service.get_bron_by_id(bron_id)
        instance.get_by_id.assert_called_once_with(bron_id)
