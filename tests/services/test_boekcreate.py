import pytest
from unittest.mock import MagicMock, patch
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import (
    BoekCreateUniqueConstraintException,
    BoekCreateValidationException,
    BoekCreateDatabaseException
)

def test_boek_create_calls_insert_sql():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    mock_cursor.lastrowid = 42
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '1234567890',
        'uitgever': 'Uitgever Naam',
        'jaar': 2024,
        'paginas': 256,
        'taal': 'Nederlands',
        'genre': 'Roman'
    }

    service = BoekService(mock_conn)
    result = service.create_boek(boek_data)

    mock_conn.cursor.assert_called_once()
    assert mock_cursor.execute.call_count == 1
    args, kwargs = mock_cursor.execute.call_args
    assert "INSERT INTO boeken" in args[0]
    assert boek_data['titel'] in args[1]
    assert result['titel'] == boek_data['titel']
    assert result['id'] == 42
    mock_conn.commit.assert_called_once()

def test_boek_create_raises_BoekCreateUniqueConstraintException_on_duplicate():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("UNIQUE constraint failed: boeken.isbn")
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '1234567890',
        'uitgever': 'Uitgever Naam',
        'jaar': 2024,
        'paginas': 256,
        'taal': 'Nederlands',
        'genre': 'Roman'
    }

    service = BoekService(mock_conn)
    with patch("src.services.boekcreate.BoekCreateUniqueConstraintException", BoekCreateUniqueConstraintException):
        with pytest.raises(BoekCreateUniqueConstraintException):
            service.create_boek(boek_data)

def test_boek_create_raises_BoekCreateValidationException_on_invalid_data():
    mock_conn = MagicMock()
    boek_data = {
        'titel': '',  # Titel is verplicht
        'auteur': 'Auteur Naam',
        'isbn': '1234567890',
        'uitgever': 'Uitgever Naam',
        'jaar': 2024,
        'paginas': 256,
        'taal': 'Nederlands',
        'genre': 'Roman'
    }
    service = BoekService(mock_conn)
    with pytest.raises(BoekCreateValidationException):
        service.create_boek(boek_data)

def test_boek_create_raises_BoekCreateDatabaseException_on_commit_failure():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    mock_cursor.lastrowid = 101
    mock_conn.commit.side_effect = Exception("Database commit failed")
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '9876543210',
        'uitgever': 'Andere Uitgever',
        'jaar': 2023,
        'paginas': 300,
        'taal': 'Nederlands',
        'genre': 'Thriller'
    }
    service = BoekService(mock_conn)
    with pytest.raises(BoekCreateDatabaseException):
        service.create_boek(boek_data)

def test_boek_create_returns_dict_with_id_on_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    mock_cursor.lastrowid = 5
    boek_data = {
        'titel': 'Boek ABC',
        'auteur': 'Auteur C',
        'isbn': '1111111111',
        'uitgever': 'Uitgever1',
        'jaar': 2022,
        'paginas': 150,
        'taal': 'Nederlands',
        'genre': 'Non-fictie'
    }
    service = BoekService(mock_conn)
    result = service.create_boek(boek_data)
    assert result['id'] == 5
    assert result['titel'] == 'Boek ABC'
    mock_conn.commit.assert_called_once()

def test_boek_create_fails_when_rowcount_zero():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    boek_data = {
        'titel': 'Titel XYZ',
        'auteur': 'Auteur Z',
        'isbn': '2222222222',
        'uitgever': 'Uitgever2',
        'jaar': 2020,
        'paginas': 99,
        'taal': 'Engels',
        'genre': 'Biografie'
    }
    service = BoekService(mock_conn)
    with pytest.raises(BoekCreateDatabaseException):
        service.create_boek(boek_data)
