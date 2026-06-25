import pytest
from unittest.mock import MagicMock
from src.services.boekupdate import BoekService
from src.services.boekupdate_exceptions import BoekNotFoundException, BoekUpdateValidationException

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def boek_service(mock_db):
    return BoekService(db_connection=mock_db)

def test_boek_update_succesvol(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    boek_id = 42
    nieuwe_data = {"titel": "Nieuwe Titel", "auteur": "Auteur X"}
    mock_cursor.rowcount = 1

    boek_service.update_boek(boek_id, nieuwe_data)

    assert mock_db.cursor.called
    sql_query = "UPDATE boeken SET titel = ?, auteur = ? WHERE id = ?"
    mock_cursor.execute.assert_called_once_with(
        sql_query,
        ("Nieuwe Titel", "Auteur X", 42)
    )
    assert mock_db.commit.called
    mock_cursor.close.assert_called_once()

def test_boek_update_boek_niet_gevonden(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    boek_id = 1
    nieuwe_data = {"titel": "Titel", "auteur": "Auteur"}
    mock_cursor.rowcount = 0

    with pytest.raises(BoekNotFoundException):
        boek_service.update_boek(boek_id, nieuwe_data)

    assert mock_db.commit.call_count == 0
    mock_cursor.close.assert_called_once()

def test_boek_update_onjuiste_data(boek_service):
    boek_id = 3
    verkeerde_data = {"titel": "Alleen Titel"}  # Verplicht veld "auteur" ontbreekt

    with pytest.raises(BoekUpdateValidationException):
        boek_service.update_boek(boek_id, verkeerde_data)

def test_update_boek_voert_juist_sql_uit(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    boek_id = 7
    nieuwe_data = {"titel": "Testboek", "auteur": "Auteur Y"}

    boek_service.update_boek(boek_id, nieuwe_data)

    mock_cursor.execute.assert_called_with(
        "UPDATE boeken SET titel = ?, auteur = ? WHERE id = ?",
        ("Testboek", "Auteur Y", 7)
    )

def test_update_rolt_terug_bij_exception(boek_service, mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor
    boek_id = 8
    nieuwe_data = {"titel": "Test", "auteur": "Auteur"}
    mock_cursor.execute.side_effect = Exception("SQL fout")

    with pytest.raises(Exception):
        boek_service.update_boek(boek_id, nieuwe_data)

    mock_db.rollback.assert_called_once()
    mock_cursor.close.assert_called_once()
