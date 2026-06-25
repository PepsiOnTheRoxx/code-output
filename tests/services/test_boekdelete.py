import pytest
from unittest.mock import MagicMock, patch
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNietGevondenException, BoekDeleteException

@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def boek_service(mock_db_connection):
    return BoekService(db_connection=mock_db_connection)

def test_delete_boek_succesvol(boek_service, mock_db_connection):
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 1

    boek_id = 42

    boek_service.delete_boek(boek_id)

    mock_db_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM boek WHERE id = ?", (boek_id,)
    )
    assert mock_cursor.rowcount == 1
    mock_db_connection.commit.assert_called_once()

def test_delete_boek_niet_gevonden(boek_service, mock_db_connection):
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 0

    boek_id = 123

    with pytest.raises(BoekNietGevondenException):
        boek_service.delete_boek(boek_id)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM boek WHERE id = ?", (boek_id,)
    )
    mock_db_connection.commit.assert_not_called()

def test_delete_boek_sql_error(boek_service, mock_db_connection):
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("DB Error")

    boek_id = 99

    with pytest.raises(BoekDeleteException):
        boek_service.delete_boek(boek_id)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM boek WHERE id = ?", (boek_id,)
    )
    mock_db_connection.commit.assert_not_called()