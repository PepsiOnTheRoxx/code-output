import pytest
from unittest.mock import MagicMock, patch
from src.services.boekdelete import BoekDeleteService
from src.services.boekdelete_exceptions import BoekNietGevondenException, BoekDeleteDatabaseException

@pytest.fixture
def mock_db_connection():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn

def test_boekdelete_verwijdert_boek_en_commit(mock_db_connection):
    cursor = mock_db_connection.cursor.return_value
    cursor.rowcount = 1
    service = BoekDeleteService(db_connection=mock_db_connection)

    service.delete_boek(42)

    mock_db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("DELETE FROM boeken WHERE id = ?", (42,))
    mock_db_connection.commit.assert_called_once()

def test_boekdelete_boeknietgevonden_raised(mock_db_connection):
    cursor = mock_db_connection.cursor.return_value
    cursor.rowcount = 0
    service = BoekDeleteService(db_connection=mock_db_connection)

    with pytest.raises(BoekNietGevondenException):
        service.delete_boek(99)
    cursor.execute.assert_called_once_with("DELETE FROM boeken WHERE id = ?", (99,))
    mock_db_connection.commit.assert_not_called()

def test_boekdelete_databasefout_exception(mock_db_connection):
    cursor = mock_db_connection.cursor.return_value
    cursor.execute.side_effect = Exception("SQL error")
    service = BoekDeleteService(db_connection=mock_db_connection)

    with pytest.raises(BoekDeleteDatabaseException):
        service.delete_boek(10)
    cursor.execute.assert_called_once_with("DELETE FROM boeken WHERE id = ?", (10,))
    mock_db_connection.commit.assert_not_called()
