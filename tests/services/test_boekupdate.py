import pytest
from unittest.mock import MagicMock, patch
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

def test_update_boek_succesvolle_update():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    service = BoekService(db_connection)
    boek_id = 42
    boek_data = {
        "titel": "Nieuw Titel",
        "auteur": "Nieuwe Auteur",
        "jaar": 2020,
        "genre": "Roman",
        "isbn": "1234567890123"
    }

    service.update_boek(boek_id, boek_data)

    db_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    query = mock_cursor.execute.call_args[0][0]
    params = mock_cursor.execute.call_args[0][1]
    assert "UPDATE boek SET" in query
    assert "WHERE id = ?" in query
    assert params[-1] == boek_id
    assert all(val in params for val in boek_data.values())
    db_connection.commit.assert_called_once()

def test_update_boek_raises_boek_niet_gevonden():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    service = BoekService(db_connection)
    boek_id = 5
    boek_data = {
        "titel": "Titel",
        "auteur": "Auteur",
        "jaar": 1999,
        "genre": "Fictie",
        "isbn": "1111111111111"
    }

    with pytest.raises(BoekNietGevondenException):
        service.update_boek(boek_id, boek_data)

    db_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    db_connection.commit.assert_not_called()

def test_update_boek_ongeldige_data_exception():
    db_connection = MagicMock()
    service = BoekService(db_connection)
    boek_id = 1
    # Onvolledige boek_data (ontbrekende verplichte velden)
    boek_data = {
        "titel": "Titel"
        # ontbrekende keys: auteur, jaar, genre, isbn
    }

    with pytest.raises(OngeldigeBoekDataException):
        service.update_boek(boek_id, boek_data)

    db_connection.cursor.assert_not_called()
    db_connection.commit.assert_not_called()

def test_update_boek_db_fout_rolback():
    db_connection = MagicMock()
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    mock_cursor.execute.side_effect = Exception("DB-fout")
    service = BoekService(db_connection)
    boek_id = 8
    boek_data = {
        "titel": "X",
        "auteur": "Y",
        "jaar": 2222,
        "genre": "Test",
        "isbn": "2222222222222"
    }

    with pytest.raises(Exception):
        service.update_boek(boek_id, boek_data)

    db_connection.rollback.assert_called_once()