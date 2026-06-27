import pytest
from unittest.mock import patch, MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseSetupException

def test_initialize_database_creates_connection_and_table():
    with patch("database.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_setup = DatabaseSetup("test.db")
        db_setup.initialize_database()

        mock_connect.assert_called_once_with("test.db")
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "CREATE TABLE IF NOT EXISTS boeken ("
            "auteur TEXT,"
            "beschrijving TEXT,"
            "isbn TEXT,"
            "publicatiedatum DATE,"
            "kaft_foto_url TEXT,"
            "is_uitgeleend BOOLEAN,"
            "uitgeleend_datum DATE,"
            "uitgeleend_max_tot DATE)"
        )
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

def test_initialize_database_raises_exception_on_connection_error():
    with patch("database.sqlite3.connect", side_effect=Exception("db error")):
        db_setup = DatabaseSetup("test_ongeldige.db")
        with pytest.raises(DatabaseSetupException):
            db_setup.initialize_database()

def test_initialize_database_raises_exception_on_execute_error():
    with patch("database.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("table error")

        db_setup = DatabaseSetup("test.db")
        with pytest.raises(DatabaseSetupException):
            db_setup.initialize_database()

def test_initialize_database_closes_connection_on_execute_error():
    with patch("database.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("fout")

        db_setup = DatabaseSetup("test.db")
        with pytest.raises(DatabaseSetupException):
            db_setup.initialize_database()
        mock_conn.close.assert_called_once()

def test_initialize_database_closes_cursor_on_success():
    with patch("database.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_setup = DatabaseSetup("test.db")
        db_setup.initialize_database()

        mock_cursor.close.assert_called_once()