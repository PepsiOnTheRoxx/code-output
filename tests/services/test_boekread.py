import pytest
from unittest.mock import MagicMock, patch
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNietGevondenException

def test_haal_boek_op_by_id_succes():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchone.return_value = (1, "Titel A", "Auteur A")
    boek_service = BoekService(db_connection)

    boek = boek_service.haal_boek_op(1)

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("SELECT id, titel, auteur FROM boeken WHERE id=?;", (1,))
    assert boek["id"] == 1
    assert boek["titel"] == "Titel A"
    assert boek["auteur"] == "Auteur A"

def test_haal_boek_op_by_id_niet_gevonden():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchone.return_value = None
    boek_service = BoekService(db_connection)

    with pytest.raises(BoekNietGevondenException):
        boek_service.haal_boek_op(999)

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("SELECT id, titel, auteur FROM boeken WHERE id=?;", (999,))

def test_haal_alle_boeken_succes():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchall.return_value = [
        (1, "Titel A", "Auteur A"),
        (2, "Titel B", "Auteur B")
    ]
    boek_service = BoekService(db_connection)

    boeken = boek_service.haal_alle_boeken()

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("SELECT id, titel, auteur FROM boeken;")
    assert len(boeken) == 2
    assert boeken[0]["id"] == 1
    assert boeken[0]["titel"] == "Titel A"
    assert boeken[0]["auteur"] == "Auteur A"
    assert boeken[1]["id"] == 2
    assert boeken[1]["titel"] == "Titel B"
    assert boeken[1]["auteur"] == "Auteur B"

def test_haal_alle_boeken_leeg():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchall.return_value = []
    boek_service = BoekService(db_connection)

    boeken = boek_service.haal_alle_boeken()

    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with("SELECT id, titel, auteur FROM boeken;")
    assert boeken == []
