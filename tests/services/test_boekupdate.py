import pytest
from unittest.mock import MagicMock, patch
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNotFoundException, BoekUpdateException

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def boek_service(mock_db):
    return BoekService(mock_db)

def test_update_boek_success(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 1

    boek_id = 5
    update_data = {"titel": "Nieuwe Titel", "auteur": "Nieuwe Auteur"}

    result = boek_service.update_boek(boek_id, update_data)

    assert result is True
    mock_db.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args
    assert "UPDATE boek" in args[0]
    assert boek_id in args[1]
    for value in update_data.values():
        assert value in args[1]
    mock_db.commit.assert_called_once()

def test_update_boek_not_found(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 0

    boek_id = 99
    update_data = {"titel": "Titel"}

    with pytest.raises(BoekNotFoundException):
        boek_service.update_boek(boek_id, update_data)

    mock_db.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_db.commit.assert_not_called()

def test_update_boek_exception_rolls_back(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL error")

    boek_id = 7
    update_data = {"titel": "Titel"}

    with pytest.raises(BoekUpdateException):
        boek_service.update_boek(boek_id, update_data)

    mock_db.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_db.rollback.assert_called_once()
    mock_db.commit.assert_not_called()

def test_update_boek_sql_query_correct(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.rowcount = 1

    boek_id = 10
    update_data = {"titel": "X", "auteur": "Y", "jaar": 2023}

    boek_service.update_boek(boek_id, update_data)

    args, kwargs = mock_cursor.execute.call_args
    query = args[0].lower()
    assert "update boek" in query
    assert "set" in query
    assert "where id" in query
    params = args[1]
    assert "X" in params
    assert "Y" in params
    assert 2023 in params
    assert boek_id in params