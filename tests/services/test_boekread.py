import pytest
from unittest.mock import MagicMock, patch
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNietGevondenException

def test_get_boek_by_id_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    boek_id = 5
    expected_result = (5, "De Ontdekking van de Hemel", "Harry Mulisch")
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = expected_result

    service = BoekService(mock_conn)
    result = service.get_boek_by_id(boek_id)

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken WHERE id = ?", (boek_id,)
    )
    mock_cursor.fetchone.assert_called_once()
    assert result == expected_result

def test_get_boek_by_id_not_found():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    boek_id = 99
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    service = BoekService(mock_conn)
    with pytest.raises(BoekNietGevondenException):
        service.get_boek_by_id(boek_id)

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken WHERE id = ?", (boek_id,)
    )
    mock_cursor.fetchone.assert_called_once()

def test_get_all_boeken_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    expected_result = [
        (1, "De avonden", "Gerard Reve"),
        (2, "Max Havelaar", "Multatuli"),
        (3, "Karakter", "F. Bordewijk"),
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = expected_result

    service = BoekService(mock_conn)
    result = service.get_all_boeken()

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken"
    )
    mock_cursor.fetchall.assert_called_once()
    assert result == expected_result

def test_get_all_boeken_none():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    service = BoekService(mock_conn)
    result = service.get_all_boeken()

    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken"
    )
    mock_cursor.fetchall.assert_called_once()
    assert result == []
