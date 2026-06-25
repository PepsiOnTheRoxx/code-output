import pytest
from unittest.mock import MagicMock, patch
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

def test_update_boek_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    service = BoekService(mock_conn)

    boek_id = 123
    boek_data = {"titel": "Nieuwe Titel", "auteur": "Nieuwe Auteur"}
    expected_query = "UPDATE boeken SET titel=?, auteur=? WHERE id=?"

    service.update_boek(boek_id, boek_data)

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        expected_query,
        (boek_data["titel"], boek_data["auteur"], boek_id)
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_update_boek_not_found_raises():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    service = BoekService(mock_conn)

    boek_id = 999
    boek_data = {"titel": "Nog Een Titel", "auteur": "Auteur"}

    with pytest.raises(BoekNietGevondenException):
        service.update_boek(boek_id, boek_data)

    expected_query = "UPDATE boeken SET titel=?, auteur=? WHERE id=?"
    mock_cursor.execute.assert_called_once_with(
        expected_query,
        (boek_data["titel"], boek_data["auteur"], boek_id)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.commit.assert_not_called()

def test_update_boek_invalid_data_raises():
    mock_conn = MagicMock()
    service = BoekService(mock_conn)

    boek_id = 10
    ongeldig_boek_data = {"titel": "", "auteur": None}

    with pytest.raises(OngeldigeBoekDataException):
        service.update_boek(boek_id, ongeldig_boek_data)

    mock_conn.cursor.assert_not_called()
    mock_conn.commit.assert_not_called()