import pytest
from unittest.mock import MagicMock
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    BoekMissingAttributeException,
    BoekInvalidAttributeException,
    BoekDatabaseException,
)

def test_create_boek_success():
    db_conn = MagicMock()
    mock_cursor = MagicMock()
    db_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Boek bestaat niet
    mock_cursor.rowcount = 1

    service = BoekService(db_conn)
    boek_data = {
        "titel": "De Avonturen",
        "auteur": "J. Auteur",
        "isbn": "1234567890",
        "jaartal": 2020,
        "categorie": "Fictie",
        "taal": "Nederlands",
        "uitgever": "BoekUitg",
        "paginas": 200,
        "prijs": 19.95
    }

    service.create_boek(boek_data)

    expected_select = "SELECT 1 FROM boeken WHERE isbn = ?"
    expected_insert = "INSERT INTO boeken (titel, auteur, isbn, jaartal, categorie, taal, uitgever, paginas, prijs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    mock_cursor.execute.assert_any_call(expected_select, ("1234567890",))
    mock_cursor.execute.assert_any_call(
        expected_insert,
        (
            "De Avonturen",
            "J. Auteur",
            "1234567890",
            2020,
            "Fictie",
            "Nederlands",
            "BoekUitg",
            200,
            19.95,
        ),
    )
    db_conn.commit.assert_called_once()

def test_create_boek_already_exists_raises():
    db_conn = MagicMock()
    mock_cursor = MagicMock()
    db_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)  # Boek bestaat al

    service = BoekService(db_conn)
    boek_data = {
        "titel": "Bestaat Al",
        "auteur": "J. Auteur",
        "isbn": "9876543210",
        "jaartal": 2022,
        "categorie": "Fictie",
        "taal": "Nederlands",
        "uitgever": "Uitg",
        "paginas": 100,
        "prijs": 12.50
    }

    with pytest.raises(BoekAlreadyExistsException):
        service.create_boek(boek_data)

    select_sql = "SELECT 1 FROM boeken WHERE isbn = ?"
    mock_cursor.execute.assert_any_call(select_sql, ("9876543210",))
    db_conn.commit.assert_not_called()

def test_create_boek_invalid_data_raises_none():
    db_conn = MagicMock()
    service = BoekService(db_conn)
    boek_data = {
        "titel": None,  # titel mag niet None zijn
        "auteur": "J. Auteur",
        "isbn": "0000",
        "jaartal": 2020,
        "categorie": "NonFictie",
        "taal": "NL",
        "uitgever": "EenUitgever",
        "paginas": 10,
        "prijs": 0
    }

    with pytest.raises(BoekInvalidAttributeException):
        service.create_boek(boek_data)

def test_create_boek_invalid_data_raises_missing():
    db_conn = MagicMock()
    service = BoekService(db_conn)
    boek_data = {
        # "titel" ontbreekt
        "auteur": "J. Auteur",
        "isbn": "0000",
        "jaartal": 2020,
        "categorie": "NonFictie",
        "taal": "NL",
        "uitgever": "EenUitgever",
        "paginas": 10,
        "prijs": 0
    }

    with pytest.raises(BoekMissingAttributeException):
        service.create_boek(boek_data)

def test_create_boek_database_exception_raises():
    db_conn = MagicMock()
    mock_cursor = MagicMock()
    db_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    # First call is select, second call is insert -> error
    mock_cursor.execute.side_effect = [None, Exception("SQL error")]
    db_conn.commit.side_effect = Exception("Commit failed")

    service = BoekService(db_conn)
    boek_data = {
        "titel": "Oeps DB",
        "auteur": "Anoniem",
        "isbn": "1122334455",
        "jaartal": 2021,
        "categorie": "Roman",
        "taal": "NL",
        "uitgever": "X Uitgever",
        "paginas": 300,
        "prijs": 22.0
    }

    with pytest.raises(BoekDatabaseException):
        service.create_boek(boek_data)
