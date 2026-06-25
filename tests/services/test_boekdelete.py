import pytest
from unittest.mock import MagicMock
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNietGevondenException, BoekDeleteDatabaseException

def test_boek_delete_succesvolle_verwijdering():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    service = BoekService(db_connection)
    boek_id = 123

    result = service.verwijder_boek(boek_id)

    db_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with('DELETE FROM boeken WHERE id = ?', (boek_id,))
    db_connection.commit.assert_called_once()
    assert result is True

def test_boek_delete_boek_niet_gevonden_raises_exception():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    service = BoekService(db_connection)
    boek_id = 999

    with pytest.raises(BoekNietGevondenException):
        service.verwijder_boek(boek_id)

    mock_cursor.execute.assert_called_once_with('DELETE FROM boeken WHERE id = ?', (boek_id,))
    db_connection.commit.assert_not_called()

def test_boek_delete_veroorzaakt_database_fout_raises_exception():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database is kapot")

    service = BoekService(db_connection)
    boek_id = 1

    with pytest.raises(BoekDeleteDatabaseException):
        service.verwijder_boek(boek_id)
        
    db_connection.commit.assert_not_called()
