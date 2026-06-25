import pytest
from unittest.mock import patch, MagicMock
from src.services.boekdeleteservice import BoekDeleteService
from src.services.boekdeleteservice_exceptions import BoekNotFoundException, DatabaseException

@pytest.fixture
def boek_repo_mock():
    with patch('src.services.boekdeleteservice.BoekRepository') as RepoMock:
        yield RepoMock.return_value

@pytest.fixture
def service(boek_repo_mock):
    return BoekDeleteService(repository=boek_repo_mock)

def test_delete_boek_succesvol(service, boek_repo_mock):
    boek_id = 123
    boek_repo_mock.exists.return_value = True
    boek_repo_mock.delete.return_value = None

    service.delete_boek(boek_id)

    boek_repo_mock.exists.assert_called_once_with(boek_id)
    boek_repo_mock.delete.assert_called_once_with(boek_id)

def test_delete_boek_bestaat_niet_werpt_exception(service, boek_repo_mock):
    boek_id = 456
    boek_repo_mock.exists.return_value = False

    with pytest.raises(BoekNotFoundException):
        service.delete_boek(boek_id)

    boek_repo_mock.exists.assert_called_once_with(boek_id)
    boek_repo_mock.delete.assert_not_called()

def test_delete_boek_database_faalt(service, boek_repo_mock):
    boek_id = 789
    boek_repo_mock.exists.return_value = True
    boek_repo_mock.delete.side_effect = DatabaseException("DB error")

    with pytest.raises(DatabaseException):
        service.delete_boek(boek_id)

    boek_repo_mock.exists.assert_called_once_with(boek_id)
    boek_repo_mock.delete.assert_called_once_with(boek_id)