import pytest
from unittest.mock import MagicMock, patch
from src.services.boekupdateservice import BoekUpdateService
from src.services.boekupdateservice_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

@pytest.fixture
def mock_conn():
    return MagicMock()

@pytest.fixture
def boek_update_service(mock_conn):
    return BoekUpdateService(db_conn=mock_conn)

def test_update_boek_succesvol(boek_update_service, mock_conn):
    boek_id = 23
    nieuwe_data = {'titel': 'Nieuwe titel', 'auteur': 'Nieuwe auteur', 'jaar': 2023}
    cursor = MagicMock()
    mock_conn.cursor.return_value = cursor

    cursor.execute.return_value = None
    cursor.rowcount = 1

    boek_update_service.update_boek(boek_id, nieuwe_data)

    cursor.execute.assert_called_with(
        "UPDATE boeken SET titel=?, auteur=?, jaar=? WHERE id=?",
        ('Nieuwe titel', 'Nieuwe auteur', 2023, 23)
    )
    mock_conn.commit.assert_called_once()

def test_update_boek_werpt_BoekNietGevondenException(boek_update_service, mock_conn):
    boek_id = 42
    nieuwe_data = {'titel': 'Niet bestaand', 'auteur': 'Onbekend', 'jaar': 2000}
    cursor = MagicMock()
    mock_conn.cursor.return_value = cursor

    cursor.execute.return_value = None
    cursor.rowcount = 0

    with pytest.raises(BoekNietGevondenException):
        boek_update_service.update_boek(boek_id, nieuwe_data)

def test_update_boek_ongeldige_data_werpt_exception(boek_update_service):
    boek_id = 5
    ongeldige_data = {'titel': 'Test', 'auteur': None, 'jaar': 'tweeduizend'}

    with pytest.raises(OngeldigeBoekDataException):
        boek_update_service.update_boek(boek_id, ongeldige_data)

def test_update_boek_sluit_cursor_correct_af(boek_update_service, mock_conn):
    boek_id = 7
    nieuwe_data = {'titel': 'Titel', 'auteur': 'Auteur', 'jaar': 2024}
    cursor = MagicMock()
    mock_conn.cursor.return_value = cursor

    cursor.rowcount = 1

    boek_update_service.update_boek(boek_id, nieuwe_data)

    assert cursor.close.called

def test_update_boek_db_exception_rollbacks(boek_update_service, mock_conn):
    boek_id = 151
    nieuwe_data = {'titel': 'Crash', 'auteur': 'Crash', 'jaar': 1999}
    cursor = MagicMock()
    mock_conn.cursor.return_value = cursor

    cursor.execute.side_effect = Exception("DB Failure")

    with pytest.raises(Exception):
        boek_update_service.update_boek(boek_id, nieuwe_data)

    mock_conn.rollback.assert_called_once()
