import pytest
from unittest.mock import MagicMock
from src.services.boekcreate import BoekCreateService
from src.services.boekcreate_exceptions import BoekCreateDuplicateException, BoekCreateDatabaseException

def test_boek_create_success():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor

    boek_data = {
        "titel": "Test Titel",
        "auteur": "Test Auteur",
        "isbn": "1234567890123",
        "publicatiejaar": 2021,
        "genre": "Fictie",
        "taal": "Nederlands",
        "uitgever": "Test Uitgever",
        "pagina_aantal": 300,
    }

    mock_cursor.fetchone.return_value = None
    mock_cursor.rowcount = 1

    service = BoekCreateService(db_connection)
    service.create_boek(boek_data)

    query_exists = "SELECT 1 FROM boeken WHERE isbn=?"
    mock_cursor.execute.assert_any_call(query_exists, (boek_data["isbn"],))

    query_insert = (
        "INSERT INTO boeken (titel, auteur, isbn, publicatiejaar, genre, taal, uitgever, pagina_aantal) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    mock_cursor.execute.assert_any_call(
        query_insert,
        (
            boek_data["titel"],
            boek_data["auteur"],
            boek_data["isbn"],
            boek_data["publicatiejaar"],
            boek_data["genre"],
            boek_data["taal"],
            boek_data["uitgever"],
            boek_data["pagina_aantal"],
        ),
    )
    db_connection.commit.assert_called_once()

def test_boek_create_boek_bestaat_al_exception():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor

    boek_data = {
        "titel": "Test Titel",
        "auteur": "Test Auteur",
        "isbn": "1234567890123",
        "publicatiejaar": 2021,
        "genre": "Fictie",
        "taal": "Nederlands",
        "uitgever": "Test Uitgever",
        "pagina_aantal": 300,
    }

    mock_cursor.fetchone.return_value = (1,)

    service = BoekCreateService(db_connection)
    with pytest.raises(BoekCreateDuplicateException):
        service.create_boek(boek_data)

    query_exists = "SELECT 1 FROM boeken WHERE isbn=?"
    mock_cursor.execute.assert_any_call(query_exists, (boek_data["isbn"],))
    db_connection.commit.assert_not_called()

def test_boek_create_aanmaken_mislukt_exception_rowcount_zero():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor

    boek_data = {
        "titel": "Test Titel",
        "auteur": "Test Auteur",
        "isbn": "1234567890123",
        "publicatiejaar": 2021,
        "genre": "Fictie",
        "taal": "Nederlands",
        "uitgever": "Test Uitgever",
        "pagina_aantal": 300,
    }

    mock_cursor.fetchone.return_value = None
    mock_cursor.rowcount = 0

    service = BoekCreateService(db_connection)
    with pytest.raises(BoekCreateDatabaseException):
        service.create_boek(boek_data)

    query_exists = "SELECT 1 FROM boeken WHERE isbn=?"
    mock_cursor.execute.assert_any_call(query_exists, (boek_data["isbn"],))

    query_insert = (
        "INSERT INTO boeken (titel, auteur, isbn, publicatiejaar, genre, taal, uitgever, pagina_aantal) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    mock_cursor.execute.assert_any_call(
        query_insert,
        (
            boek_data["titel"],
            boek_data["auteur"],
            boek_data["isbn"],
            boek_data["publicatiejaar"],
            boek_data["genre"],
            boek_data["taal"],
            boek_data["uitgever"],
            boek_data["pagina_aantal"],
        ),
    )
    db_connection.commit.assert_not_called()

def test_boek_create_rollback_on_db_exception():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor

    boek_data = {
        "titel": "Titel",
        "auteur": "Auteur",
        "isbn": "1234567890123",
        "publicatiejaar": 2023,
        "genre": "Thriller",
        "taal": "Nederlands",
        "uitgever": "Uitgever",
        "pagina_aantal": 250,
    }

    mock_cursor.fetchone.return_value = None
    mock_cursor.execute.side_effect = [None, Exception("DB failure")]

    service = BoekCreateService(db_connection)
    with pytest.raises(BoekCreateDatabaseException):
        service.create_boek(boek_data)

    db_connection.rollback.assert_called_once()
    db_connection.commit.assert_not_called()
