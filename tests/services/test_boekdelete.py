import pytest
from unittest.mock import MagicMock, patch
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNotFoundException, BoekDeleteException

def test_delete_boek_success():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value.__enter__.return_value = cursor
    cursor.rowcount = 1

    service = BoekService(db_connection)
    boek_id = 123

    result = service.delete_boek(boek_id)

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("DELETE FROM boeken WHERE id = %s", (boek_id,))
    assert result is True

def test_delete_boek_not_found():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value.__enter__.return_value = cursor
    cursor.rowcount = 0

    service = BoekService(db_connection)
    boek_id = 456

    with pytest.raises(BoekNotFoundException):
        service.delete_boek(boek_id)

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("DELETE FROM boeken WHERE id = %s", (boek_id,))

def test_delete_boek_sql_error():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value.__enter__.return_value = cursor
    cursor.execute.side_effect = Exception("SQL error")

    service = BoekService(db_connection)
    boek_id = 789

    with pytest.raises(BoekDeleteException):
        service.delete_boek(boek_id)

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("DELETE FROM boeken WHERE id = %s", (boek_id,))