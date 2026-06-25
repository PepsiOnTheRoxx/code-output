import pytest
from unittest.mock import MagicMock, patch
from src.services.boekdeleteservice import BoekDeleteService
from src.services.boekdeleteservice_exceptions import BoekNotFoundException, DatabaseDeleteException

@pytest.fixture
def mock_connection():
    return MagicMock()

@pytest.fixture
def boek_delete_service(mock_connection):
    return BoekDeleteService(db_connection=mock_connection)

def test_verwijder_boek_succesvol(boek_delete_service, mock_connection):
    cursor_mock = MagicMock()
    mock_connection.cursor.return_value = cursor_mock
    cursor_mock.rowcount = 1

    boek_id = 42
    result = boek_delete_service.verwijder_boek(boek_id)

    mock_connection.cursor.assert_called_once()
    cursor_mock.execute.assert_called_once_with("DELETE FROM boeken WHERE id=?", (boek_id,))
    mock_connection.commit.assert_called_once()
    assert result is True

def test_verwijder_boek_niet_gevonden(boek_delete_service, mock_connection):
    cursor_mock = MagicMock()
    mock_connection.cursor.return_value = cursor_mock
    cursor_mock.rowcount = 0

    boek_id = 777
    with pytest.raises(BoekNotFoundException):
        boek_delete_service.verwijder_boek(boek_id)

    mock_connection.cursor.assert_called_once()
    cursor_mock.execute.assert_called_once_with("DELETE FROM boeken WHERE id=?", (boek_id,))
    mock_connection.commit.assert_not_called()

def test_verwijder_boek_database_fout(boek_delete_service, mock_connection):
    cursor_mock = MagicMock()
    mock_connection.cursor.return_value = cursor_mock
    cursor_mock.execute.side_effect = Exception("database error")

    boek_id = 12
    with pytest.raises(DatabaseDeleteException):
        boek_delete_service.verwijder_boek(boek_id)

    mock_connection.cursor.assert_called_once()
    cursor_mock.execute.assert_called_once_with("DELETE FROM boeken WHERE id=?", (boek_id,))
    mock_connection.commit.assert_not_called()