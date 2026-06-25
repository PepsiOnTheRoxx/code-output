import pytest
from unittest.mock import MagicMock, patch
from src.services.boekread import BoekService, DatabaseException
from src.services.boekread_exceptions import BoekNotFoundException

def test_get_boek_by_id_executes_correct_query_and_returns_boek():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchone.return_value = (
        1, "De Ontdekking van de Hemel", "Harry Mulisch", 1992, "Roman"
    )
    service = BoekService(db_connection)
    boek = service.get_boek_by_id(1)
    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur, jaar, genre FROM boeken WHERE id = ?", (1,)
    )
    assert boek.id == 1
    assert boek.titel == "De Ontdekking van de Hemel"
    assert boek.auteur == "Harry Mulisch"
    assert boek.jaar == 1992
    assert boek.genre == "Roman"

def test_get_boek_by_id_not_found_raises_exception():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchone.return_value = None
    service = BoekService(db_connection)
    with pytest.raises(BoekNotFoundException):
        service.get_boek_by_id(999)

def test_get_boek_by_id_database_error_raises_databaseexception():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("database failure")
    service = BoekService(db_connection)
    with pytest.raises(DatabaseException):
        service.get_boek_by_id(1)

def test_get_all_boeken_returns_list_of_boeken():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.fetchall.return_value = [
        (1, "De Ontdekking van de Hemel", "Harry Mulisch", 1992, "Roman"),
        (2, "Het Diner", "Herman Koch", 2009, "Roman"),
    ]
    service = BoekService(db_connection)
    boeken = service.get_all_boeken()
    db_connection.cursor.assert_called_once()
    cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur, jaar, genre FROM boeken"
    )
    assert len(boeken) == 2
    assert boeken[0].titel == "De Ontdekking van de Hemel"
    assert boeken[1].titel == "Het Diner"

def test_get_all_boeken_database_error_raises_databaseexception():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("db error")
    service = BoekService(db_connection)
    with pytest.raises(DatabaseException):
        service.get_all_boeken()
