import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseSetupError

def test_create_database_and_table_success(tmp_path):
    db_path = tmp_path / "testdb.sqlite"
    setup = DatabaseSetup(str(db_path))
    setup.create_database_and_table()
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(boeken)")
    columns = [col[1] for col in cur.fetchall()]
    expected_columns = [
        "auteur",
        "beschrijving",
        "is_uitgeleend",
        "isbn",
        "kaft_foto_url",
        "publicatiedatum",
        "titel",
        "uitgeleend_datum",
        "uitgeleend_max_tot",
    ]
    assert set(columns) == set(expected_columns)
    conn.close()

def test_create_database_and_table_runs_twice_is_idempotent(tmp_path):
    db_path = tmp_path / "idempotent.sqlite"
    setup = DatabaseSetup(str(db_path))
    setup.create_database_and_table()
    # Second call should pass without errors (table already exists)
    setup.create_database_and_table()
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM boeken")
    conn.close()

def test_create_database_and_table_sqlite_error():
    with patch("sqlite3.connect", side_effect=sqlite3.OperationalError("could not open database file")):
        setup = DatabaseSetup("invalid_path/test.db")
        with pytest.raises(DatabaseSetupError):
            setup.create_database_and_table()

def test_create_database_and_table_table_schema(tmp_path):
    db_path = tmp_path / "schema_check.sqlite"
    setup = DatabaseSetup(str(db_path))
    setup.create_database_and_table()
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(boeken)")
    info = cur.fetchall()
    col_info = {col[1]: col[2] for col in info}
    assert col_info["auteur"].upper().startswith("TEXT")
    assert col_info["beschrijving"].upper().startswith("TEXT")
    assert col_info["is_uitgeleend"].upper() in ("BOOLEAN", "INTEGER")
    assert col_info["isbn"].upper().startswith("TEXT")
    assert col_info["kaft_foto_url"].upper().startswith("TEXT")
    assert col_info["publicatiedatum"].upper().startswith("DATE")
    assert col_info["titel"].upper().startswith("TEXT")
    assert col_info["uitgeleend_datum"].upper().startswith("DATE")
    assert col_info["uitgeleend_max_tot"].upper().startswith("DATE")
    conn.close()

def test_create_database_and_table_closes_connection_on_success(tmp_path):
    db_path = tmp_path / "closecheck.sqlite"
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        setup = DatabaseSetup(str(db_path))
        setup.create_database_and_table()
        assert mock_conn.close.called

def test_create_database_and_table_closes_connection_on_exception(tmp_path):
    db_path = tmp_path / "failclose.sqlite"
    with patch("sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.side_effect = sqlite3.DatabaseError("cursor error")
        setup = DatabaseSetup(str(db_path))
        with pytest.raises(DatabaseSetupError):
            setup.create_database_and_table()
        assert mock_conn.close.called
