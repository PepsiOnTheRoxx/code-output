import pytest
from unittest.mock import MagicMock
from src.services.boekupdate import BoekUpdateService
from src.services.boekupdate_exceptions import BoekNietGevondenException, BoekUpdateException

@pytest.fixture
def mock_db_conn():
    return MagicMock()

@pytest.fixture
def boek_update_service(mock_db_conn):
    return BoekUpdateService(mock_db_conn)

def test_update_boek_success(boek_update_service, mock_db_conn):
    mock_cursor = MagicMock()
    mock_db_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    boek_id = 42
    boek_data = {'titel': 'Nieuw Titel', 'auteur': 'Auteur X', 'isbn': '1234'}
    sql = "UPDATE boeken SET titel=?, auteur=?, isbn=? WHERE id=?"
    params = (boek_data['titel'], boek_data['auteur'], boek_data['isbn'], boek_id)

    boek_update_service.update_boek(boek_id, boek_data)

    mock_db_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(sql, params)
    mock_db_conn.commit.assert_called_once()

def test_update_boek_not_found(boek_update_service, mock_db_conn):
    mock_cursor = MagicMock()
    mock_db_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    boek_id = 99
    boek_data = {'titel': 'Onbestaand', 'auteur': 'Niemand', 'isbn': 'X'}
    
    with pytest.raises(BoekNietGevondenException):
        boek_update_service.update_boek(boek_id, boek_data)

    mock_db_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_db_conn.commit.assert_not_called()
    mock_db_conn.rollback.assert_called_once()

def test_update_boek_exception_on_db_error(boek_update_service, mock_db_conn):
    mock_cursor = MagicMock()
    mock_db_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("DB error")

    boek_id = 7
    boek_data = {'titel': 'Crash', 'auteur': 'Fout', 'isbn': 'ERR'}

    with pytest.raises(BoekUpdateException):
        boek_update_service.update_boek(boek_id, boek_data)

    mock_db_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_db_conn.commit.assert_not_called()
    mock_db_conn.rollback.assert_called_once()
