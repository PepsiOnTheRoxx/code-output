import pytest
from unittest.mock import MagicMock, patch
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNietGevondenException, DatabaseFoutException

def test_get_boek_returns_boek_dict():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor

    boek_data = (1, "Een boek titel", "Auteur Naam", 1999)
    cursor.fetchone.return_value = boek_data

    service = BoekService(db_conn)
    result = service.get_boek(1)

    cursor.execute.assert_called_once_with("SELECT id, titel, auteur, jaar FROM boeken WHERE id = %s", (1,))
    assert result == {
        "id": 1,
        "titel": "Een boek titel",
        "auteur": "Auteur Naam",
        "jaar": 1999
    }

def test_get_boek_raises_boek_niet_gevonden():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor

    cursor.fetchone.return_value = None

    service = BoekService(db_conn)
    with pytest.raises(BoekNietGevondenException):
        service.get_boek(42)

    cursor.execute.assert_called_once_with("SELECT id, titel, auteur, jaar FROM boeken WHERE id = %s", (42,))

def test_get_boek_raises_databasefout_bij_exception():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor

    cursor.execute.side_effect = Exception("DB error")

    service = BoekService(db_conn)
    with pytest.raises(DatabaseFoutException):
        service.get_boek(4)

def test_get_all_boeken_returns_list_of_dicts():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor

    boek_list = [
        (1, "Boek A", "Auteur A", 2001),
        (2, "Boek B", "Auteur B", 2002)
    ]
    cursor.fetchall.return_value = boek_list

    service = BoekService(db_conn)
    result = service.get_all_boeken()

    cursor.execute.assert_called_once_with("SELECT id, titel, auteur, jaar FROM boeken")
    assert isinstance(result, list)
    assert result == [
        {"id": 1, "titel": "Boek A", "auteur": "Auteur A", "jaar": 2001},
        {"id": 2, "titel": "Boek B", "auteur": "Auteur B", "jaar": 2002}
    ]

def test_get_all_boeken_empty_list():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor

    cursor.fetchall.return_value = []

    service = BoekService(db_conn)
    result = service.get_all_boeken()

    cursor.execute.assert_called_once_with("SELECT id, titel, auteur, jaar FROM boeken")
    assert result == []

def test_get_all_boeken_raises_databasefout_bij_exception():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor

    cursor.execute.side_effect = Exception("DB error")

    service = BoekService(db_conn)
    with pytest.raises(DatabaseFoutException):
        service.get_all_boeken()
