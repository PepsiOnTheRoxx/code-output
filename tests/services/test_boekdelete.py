import pytest
from unittest.mock import patch, MagicMock
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNotFoundException, BoekDeleteException

def test_delete_boek_success():
    boek_id = 1
    with patch("src.services.boekdelete.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id.return_value = MagicMock()
        boek_service = BoekService()
        boek_service._repo = mock_repo_instance

        boek_service.delete_boek(boek_id)

        mock_repo_instance.get_by_id.assert_called_once_with(boek_id)
        mock_repo_instance.delete.assert_called_once_with(boek_id)

def test_delete_boek_not_found():
    boek_id = 321
    with patch("src.services.boekdelete.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id.return_value = None
        boek_service = BoekService()
        boek_service._repo = mock_repo_instance

        with pytest.raises(BoekNotFoundException):
            boek_service.delete_boek(boek_id)

def test_delete_boek_delete_raises_exception():
    boek_id = 2
    with patch("src.services.boekdelete.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id.return_value = MagicMock()
        mock_repo_instance.delete.side_effect = Exception("db error")
        boek_service = BoekService()
        boek_service._repo = mock_repo_instance

        with pytest.raises(BoekDeleteException):
            boek_service.delete_boek(boek_id)

def test_delete_boek_calls_correct_repo_methods():
    boek_id = 42
    with patch("src.services.boekdelete.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_boek = MagicMock()
        mock_repo_instance.get_by_id.return_value = mock_boek
        boek_service = BoekService()
        boek_service._repo = mock_repo_instance

        boek_service.delete_boek(boek_id)

        assert mock_repo_instance.get_by_id.call_count == 1
        assert mock_repo_instance.delete.call_count == 1

def test_delete_boek_with_invalid_id_type():
    boek_id = "invalid-id"
    with patch("src.services.boekdelete.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        boek_service = BoekService()
        boek_service._repo = mock_repo_instance

        with pytest.raises((TypeError, BoekNotFoundException)):
            boek_service.delete_boek(boek_id)