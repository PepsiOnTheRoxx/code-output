import pytest
from unittest.mock import patch, MagicMock
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNotFoundException, BoekDeleteDatabaseException

@pytest.fixture
def boek_id():
    return 42

def test_boek_delete_succes(boek_id):
    with patch("src.services.boekdelete.BoekRepository") as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.verwijder_boek.return_value = True

        service = BoekService()
        result = service.verwijder_boek(boek_id)

        mock_repo.verwijder_boek.assert_called_once_with(boek_id)
        assert result is True

def test_boek_delete_bestaat_niet(boek_id):
    with patch("src.services.boekdelete.BoekRepository") as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.verwijder_boek.side_effect = BoekNotFoundException()

        service = BoekService()
        with pytest.raises(BoekNotFoundException):
            service.verwijder_boek(boek_id)
        mock_repo.verwijder_boek.assert_called_once_with(boek_id)

def test_boek_delete_database_exception(boek_id):
    with patch("src.services.boekdelete.BoekRepository") as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.verwijder_boek.side_effect = BoekDeleteDatabaseException("Database fout")

        service = BoekService()
        with pytest.raises(BoekDeleteDatabaseException):
            service.verwijder_boek(boek_id)
        mock_repo.verwijder_boek.assert_called_once_with(boek_id)
