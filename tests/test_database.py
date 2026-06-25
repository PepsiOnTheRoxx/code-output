import pytest
from unittest.mock import MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseInitializationError

def test_init_initialiseert_cursor():
    mock_conn = MagicMock()
    db_setup = DatabaseSetup(mock_conn)
    assert db_setup.db_connection == mock_conn

def test_initialiseer_database_maakt_tabel_aan():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    db_setup = DatabaseSetup(mock_conn)
    db_setup.initialiseer_database()

    create_table_query = (
        "CREATE TABLE IF NOT EXISTS Boek "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "titel TEXT NOT NULL, "
        "auteur TEXT NOT NULL, "
        "isbn TEXT NOT NULL, "
        "uitgever TEXT NOT NULL, "
        "publicatiejaar INTEGER, "
        "genre TEXT, "
        "taal TEXT, "
        "paginas INTEGER, "
        "beschikbaar INTEGER DEFAULT 1)"
    )
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_with(create_table_query)
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_initialiseer_database_raise_bij_sqlfout():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL Fout")

    db_setup = DatabaseSetup(mock_conn)

    with pytest.raises(DatabaseInitializationError):
        db_setup.initialiseer_database()
    mock_conn.cursor.assert_called_once()
    mock_conn.commit.assert_not_called()
    mock_cursor.close.assert_called_once()

def test_initialiseer_database_sluit_cursor_bij_exception():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL Fout")

    db_setup = DatabaseSetup(mock_conn)

    with pytest.raises(DatabaseInitializationError):
        db_setup.initialiseer_database()
    mock_cursor.close.assert_called_once()

def test_initialiseer_database_commit_alleen_bij_succes():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = None

    db_setup = DatabaseSetup(mock_conn)
    db_setup.initialiseer_database()

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
