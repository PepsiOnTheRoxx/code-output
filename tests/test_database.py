import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseSetupException

@pytest.fixture
def mock_connection():
    conn = MagicMock(spec=sqlite3.Connection)
    return conn

def test_setup_database_creates_boeken_table_with_correct_schema(monkeypatch, mock_connection):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    mock_connect = MagicMock(return_value=mock_connection)
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    db_file = ":memory:"
    setup = DatabaseSetup(db_file)
    setup.setup()

    assert mock_connect.called
    assert mock_connection.cursor.called
    expected_stmt = (
        "CREATE TABLE IF NOT EXISTS boeken ("
        "auteur TEXT, "
        "beschrijving TEXT, "
        "is_uitgeleend BOOLEAN, "
        "isbn TEXT, "
        "kaft_foto_url TEXT, "
        "publicatiedatum DATE, "
        "titel TEXT, "
        "uitgeleend_datum DATE, "
        "uitgeleend_max_tot DATE"
        ")"
    )
    mock_cursor.execute.assert_any_call(expected_stmt)
    assert mock_connection.commit.called
    assert mock_connection.close.called

def test_setup_database_raises_exception_on_sql_error(monkeypatch, mock_connection):
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.OperationalError("SQL error")
    mock_connection.cursor.return_value = mock_cursor

    mock_connect = MagicMock(return_value=mock_connection)
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    db_file = ":memory:"
    setup = DatabaseSetup(db_file)

    with pytest.raises(DatabaseSetupException):
        setup.setup()

def test_setup_database_closes_connection_on_exception(monkeypatch, mock_connection):
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = sqlite3.OperationalError("SQL error")
    mock_connection.cursor.return_value = mock_cursor

    mock_connect = MagicMock(return_value=mock_connection)
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    db_file = ":memory:"
    setup = DatabaseSetup(db_file)
    with pytest.raises(DatabaseSetupException):
        setup.setup()
    assert mock_connection.close.called

def test_setup_database_call_sequence(monkeypatch, mock_connection):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    mock_connect = MagicMock(return_value=mock_connection)
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    db_file = ":memory:"
    setup = DatabaseSetup(db_file)
    setup.setup()

    cursor_calls = mock_connection.method_calls
    assert ("cursor", (), {}) in cursor_calls
    assert ("commit", (), {}) in cursor_calls
    assert ("close", (), {}) in cursor_calls

def test_setup_database_idempotency(monkeypatch, mock_connection):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    mock_connect = MagicMock(return_value=mock_connection)
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    db_file = ":memory:"
    setup = DatabaseSetup(db_file)
    setup.setup()
    setup.setup()
    expected_stmt = (
        "CREATE TABLE IF NOT EXISTS boeken ("
        "auteur TEXT, "
        "beschrijving TEXT, "
        "is_uitgeleend BOOLEAN, "
        "isbn TEXT, "
        "kaft_foto_url TEXT, "
        "publicatiedatum DATE, "
        "titel TEXT, "
        "uitgeleend_datum DATE, "
        "uitgeleend_max_tot DATE"
        ")"
    )
    assert mock_cursor.execute.call_count == 2
    mock_cursor.execute.assert_called_with(expected_stmt)