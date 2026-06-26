import pytest
from unittest.mock import patch, MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseSetupError

@patch("database.sqlite3.connect")
def test_initialize_creates_database_and_boeken_table(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    ds = DatabaseSetup("bibliotheek.db")
    ds.initialize()

    mock_connect.assert_called_once_with("bibliotheek.db")
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call(
        """CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            isbn TEXT,
            publicatiedatum DATE,
            kaft_foto_url TEXT,
            is_uitgeleend BOOLEAN,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )"""
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("database.sqlite3.connect")
def test_initialize_raises_exception_on_failure(mock_connect):
    mock_connect.side_effect = Exception("could not connect")
    ds = DatabaseSetup("bibliotheek.db")
    with pytest.raises(DatabaseSetupError):
        ds.initialize()

@patch("database.sqlite3.connect")
def test_initialize_table_creation_failure_raises_database_setup_error(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL failed")
    ds = DatabaseSetup("bibliotheek.db")
    with pytest.raises(DatabaseSetupError):
        ds.initialize()

@patch("database.sqlite3.connect")
def test_initialize_closes_connection_on_exception(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception()
    ds = DatabaseSetup("bibliotheek.db")
    with pytest.raises(DatabaseSetupError):
        ds.initialize()
    mock_conn.close.assert_called_once()

@patch("database.sqlite3.connect")
def test_initialize_idempotent_table_creation(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    ds = DatabaseSetup("bibliotheek.db")
    # Eerste initialisatie
    ds.initialize()
    # Tweede initialisatie (moet niet falen, idem SQL)
    ds.initialize()

    assert mock_cursor.execute.call_count == 2
    args, _ = mock_cursor.execute.call_args
    assert "CREATE TABLE IF NOT EXISTS boeken" in args[0]