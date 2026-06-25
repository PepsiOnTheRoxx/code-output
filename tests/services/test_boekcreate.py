import pytest
from unittest.mock import patch, MagicMock
from datetime import date

from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekCreateException

@pytest.fixture
def boek_data():
    return {
        'auteur': 'Arnon Grunberg',
        'beschrijving': 'Een fascinerende roman.',
        'isbn': '9789020404450',
        'publicatiedatum': date(2021, 5, 10),
        'kaft_foto_url': 'https://example.com/kaft.jpg',
        'is_uitgeleend': False,
        'uitgeleend_datum': None,
        'uitgeleend_max_tot': None
    }

@patch("src.services.boekcreate.get_db")
def test_boek_create_success(mock_get_db, boek_data):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.lastrowid = 42

    service = BoekService()
    boek_id = service.create_boek(**boek_data)
    assert boek_id == 42
    mock_db.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args
    assert "INSERT INTO boeken" in args[0]
    for col in boek_data:
        assert col in args[0] or (col == 'kaft_foto_url' and 'kaft_foto_url' in args[0])
    assert tuple(boek_data.values()) == args[1]
    mock_db.commit.assert_called_once()

@patch("src.services.boekcreate.get_db")
def test_boek_create_missing_required_field(mock_get_db, boek_data):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    boek_data_copy = dict(boek_data)
    boek_data_copy.pop('auteur')
    service = BoekService()
    with pytest.raises(BoekCreateException):
        service.create_boek(**boek_data_copy)

@patch("src.services.boekcreate.get_db")
def test_boek_create_invalid_date_type(mock_get_db, boek_data):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    boek_data['publicatiedatum'] = '10-05-2021'  # Ongeldig type
    service = BoekService()
    with pytest.raises(BoekCreateException):
        service.create_boek(**boek_data)

@patch("src.services.boekcreate.get_db")
def test_boek_create_database_error(mock_get_db, boek_data):
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("DB error")
    mock_get_db.return_value = mock_db
    service = BoekService()
    with pytest.raises(BoekCreateException):
        service.create_boek(**boek_data)

@patch("src.services.boekcreate.get_db")
def test_boek_create_default_values(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.lastrowid = 5

    boek_data = {
        'auteur': 'Nescio',
        'beschrijving': '',
        'isbn': '1234567890',
        'publicatiedatum': date(2001, 1, 1),
        'kaft_foto_url': '',
        'is_uitgeleend': False,
        'uitgeleend_datum': None,
        'uitgeleend_max_tot': None
    }

    service = BoekService()
    boek_id = service.create_boek(**boek_data)
    assert boek_id == 5
    mock_db.commit.assert_called_once()
    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args
    assert "INSERT INTO boeken" in args[0]
    for col in boek_data:
        assert col in args[0] or (col == 'kaft_foto_url' and 'kaft_foto_url' in args[0])
    assert tuple(boek_data.values()) == args[1]
