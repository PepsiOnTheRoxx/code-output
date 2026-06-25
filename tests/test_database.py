import pytest
from unittest.mock import patch, MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseSetupError

@patch("database.sqlite3.connect")
def test_initialiseert_db_en_maakt_boek_tabel_aan(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    db_setup = DatabaseSetup("bibliotheek.db")
    db_setup.initialiseer_database()

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
def test_fout_bij_verbinden_met_db_raised_exception(mock_connect):
    mock_connect.side_effect = Exception("Disk error")
    db_setup = DatabaseSetup("bibliotheek.db")

    with pytest.raises(DatabaseSetupError):
        db_setup.initialiseer_database()

@patch("database.sqlite3.connect")
def test_fout_bij_tabel_aanmaken_rollback_and_raise(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Table syntax error")

    db_setup = DatabaseSetup("bibliotheek.db")

    with pytest.raises(DatabaseSetupError):
        db_setup.initialiseer_database()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("database.sqlite3.connect")
def test_initialiseren_db_is_idempotent(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    db_setup = DatabaseSetup("bibliotheek.db")
    db_setup.initialiseer_database()
    db_setup.initialiseer_database()

    assert mock_cursor.execute.call_count == 2
    calls = [
        (
            """CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            isbn TEXT,
            publicatiedatum DATE,
            kaft_foto_url TEXT,
            is_uitgeleend BOOLEAN,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )""",
        ),
        (
            """CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            isbn TEXT,
            publicatiedatum DATE,
            kaft_foto_url TEXT,
            is_uitgeleend BOOLEAN,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )""",
        ),
    ]
    mock_cursor.execute.assert_has_calls(calls)