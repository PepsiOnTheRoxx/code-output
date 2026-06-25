import pytest
from unittest.mock import patch, MagicMock
from src.services.boekreadservice import BoekReadService
from src.services.boekreadservice_exceptions import BoekNotFoundException, DatabaseReadException

def test_get_boek_by_id_succes():
    boek_id = 1
    expected_boek = {"id": 1, "titel": "Het Boek", "auteur": "Auteur"}
    with patch("src.services.boekreadservice.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "Het Boek", "Auteur")
        service = BoekReadService("test.db")
        result = service.get_boek_by_id(boek_id)
        assert result == expected_boek
        mock_cursor.execute.assert_called_with("SELECT id, titel, auteur FROM boeken WHERE id = ?", (boek_id,))

def test_get_boek_by_id_not_found():
    boek_id = 999
    with patch("src.services.boekreadservice.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        service = BoekReadService("test.db")
        with pytest.raises(BoekNotFoundException):
            service.get_boek_by_id(boek_id)

def test_get_all_boeken_success():
    expected_boeken = [
        {"id": 1, "titel": "Boek A", "auteur": "Auteur A"},
        {"id": 2, "titel": "Boek B", "auteur": "Auteur B"},
    ]
    db_rows = [
        (1, "Boek A", "Auteur A"),
        (2, "Boek B", "Auteur B")
    ]
    with patch("src.services.boekreadservice.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = db_rows
        service = BoekReadService("test.db")
        result = service.get_all_boeken()
        assert result == expected_boeken
        mock_cursor.execute.assert_called_with("SELECT id, titel, auteur FROM boeken")

def test_get_boek_by_id_database_exception():
    boek_id = 2
    with patch("src.services.boekreadservice.sqlite3.connect", side_effect=Exception("db error")):
        service = BoekReadService("test.db")
        with pytest.raises(DatabaseReadException):
            service.get_boek_by_id(boek_id)

def test_get_all_boeken_database_exception():
    with patch("src.services.boekreadservice.sqlite3.connect", side_effect=Exception("db error")):
        service = BoekReadService("test.db")
        with pytest.raises(DatabaseReadException):
            service.get_all_boeken()