import pytest
from unittest.mock import patch, MagicMock
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekAlreadyExistsException, InvalidBoekDataException

@pytest.fixture
def mock_boek_repository():
    with patch("src.services.boekcreate.BoekRepository") as repo_cls:
        yield repo_cls.return_value

@pytest.fixture
def boek_service(mock_boek_repository):
    return BoekService(repository=mock_boek_repository)

def test_create_boek_success(boek_service, mock_boek_repository):
    boek_data = {"titel": "Test Boek", "auteur": "Jan Jansen"}
    mock_boek = MagicMock()
    mock_boek_repository.exists.return_value = False
    mock_boek_repository.save.return_value = mock_boek

    result = boek_service.create_boek(boek_data)

    mock_boek_repository.exists.assert_called_once_with(boek_data)
    mock_boek_repository.save.assert_called_once_with(boek_data)
    assert result == mock_boek

def test_create_boek_already_exists_raises_exception(boek_service, mock_boek_repository):
    boek_data = {"titel": "Bestaat Al", "auteur": "Jannie"}
    mock_boek_repository.exists.return_value = True

    with pytest.raises(BoekAlreadyExistsException):
        boek_service.create_boek(boek_data)

    mock_boek_repository.exists.assert_called_once_with(boek_data)
    mock_boek_repository.save.assert_not_called()

def test_create_boek_invalid_data_raises_exception(boek_service, mock_boek_repository):
    invalid_boek_data = {"titel": ""}  # Auteur ontbreekt bijv.

    with pytest.raises(InvalidBoekDataException):
        boek_service.create_boek(invalid_boek_data)

    mock_boek_repository.exists.assert_not_called()
    mock_boek_repository.save.assert_not_called()

def test_create_boek_repository_save_failure(boek_service, mock_boek_repository):
    boek_data = {"titel": "Crash Boek", "auteur": "Piet"}
    mock_boek_repository.exists.return_value = False
    mock_boek_repository.save.side_effect = Exception("Database fout")

    with pytest.raises(Exception) as exc:
        boek_service.create_boek(boek_data)

    assert "Database fout" in str(exc.value)
    mock_boek_repository.exists.assert_called_once_with(boek_data)
    mock_boek_repository.save.assert_called_once_with(boek_data)