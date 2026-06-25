import pytest
from unittest.mock import MagicMock, patch
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNotFoundException, BoekDeleteException

def test_boek_delete_success():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 1

    service = BoekService(db_connection=mock_connection)
    boek_id = 123

    service.delete_boek(boek_id)

    mock_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM boeken WHERE id = ?", (boek_id,)
    )
    mock_connection.commit.assert_called_once()

def test_boek_delete_not_found():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 0

    service = BoekService(db_connection=mock_connection)
    boek_id = 456

    with pytest.raises(BoekNotFoundException):
        service.delete_boek(boek_id)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM boeken WHERE id = ?", (boek_id,)
    )
    mock_connection.commit.assert_not_called()

def test_boek_delete_sql_exception():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL error")

    service = BoekService(db_connection=mock_connection)
    boek_id = 789

    with pytest.raises(BoekDeleteException):
        service.delete_boek(boek_id)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM boeken WHERE id = ?", (boek_id,)
    )
    mock_connection.commit.assert_not_called()