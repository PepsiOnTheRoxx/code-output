import os
import sqlite3
import pytest
from unittest.mock import patch, MagicMock, call

import database
import database_exceptions


def test_db_path_constant_exists():
    assert hasattr(database, "DB_PATH")
    assert isinstance(database.DB_PATH, str)
    assert database.DB_PATH.endswith(".db")


def test_get_connection_calls_sqlite3_connect(monkeypatch):
    fake_connect = MagicMock()
    monkeypatch.setattr(sqlite3, "connect", fake_connect)
    fake_path = "dummy_path.db"
    monkeypatch.setattr(database, "DB_PATH", fake_path)
    conn = database.get_connection()
    fake_connect.assert_called_once_with(fake_path)
    assert conn == fake_connect.return_value


def test_get_connection_returns_connection_object(monkeypatch):
    class DummyConn:
        pass
    monkeypatch.setattr(sqlite3, "connect", lambda path: DummyConn())
    monkeypatch.setattr(database, "DB_PATH", "test.db")
    conn = database.get_connection()
    assert isinstance(conn, DummyConn)


def test_init_db_creates_table_if_not_exists(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(database, "get_connection", lambda: mock_conn)
    database.init_db()
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call(
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
    mock_conn.close.assert_called_once()


def test_init_db_error_handling(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = sqlite3.OperationalError("some db error")
    monkeypatch.setattr(database, "get_connection", lambda: mock_conn)
    with pytest.raises(database_exceptions.DatabaseSetupError):
        database.init_db()
    mock_conn.close.assert_called_once()


def test_get_connection_raises_custom_exception(monkeypatch):
    def raise_error(path):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", raise_error)
    monkeypatch.setattr(database, "DB_PATH", "fail.db")
    with pytest.raises(database_exceptions.DatabaseSetupError):
        database.get_connection()


def test_init_db_creates_correct_schema(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(database, "get_connection", lambda: mock_conn)
    database.init_db()
    sql = (
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
    mock_cursor.execute.assert_any_call(sql)


def test_init_db_commits_and_closes_even_on_exception(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("fail")
    monkeypatch.setattr(database, "get_connection", lambda: mock_conn)
    with pytest.raises(database_exceptions.DatabaseSetupError):
        database.init_db()
    mock_conn.close.assert_called_once()