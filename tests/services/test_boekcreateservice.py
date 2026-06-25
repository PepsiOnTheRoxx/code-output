import pytest
from unittest.mock import patch, MagicMock
from src.services.boekcreateservice import BoekCreateService
from src.services.boekcreateservice_exceptions import BoekCreateException

def test_create_boek_success():
    mock_db = MagicMock()
    boek_data = {
        'titel': 'De Donkere Kamer',
        'auteur': 'Willem Frederik Hermans',
        'isbn': '9789023461212',
        'uitgever': 'De Bezige Bij',
        'publicatiejaar': 1958,
        'genre': 'Roman',
        'taal': 'Nederlands',
        'pagina_aantal': 256
    }
    with patch('src.services.boekcreateservice.get_db', return_value=mock_db):
        service = BoekCreateService()
        result = service.create_boek(boek_data)
        assert result is not None
        assert isinstance(result, dict)
        assert result['titel'] == 'De Donkere Kamer'
        mock_db.execute.assert_called()

def test_create_boek_missing_required_attribute():
    mock_db = MagicMock()
    boek_data = {
        'auteur': 'Willem Frederik Hermans',
        'isbn': '9789023461212',
        'uitgever': 'De Bezige Bij',
        'publicatiejaar': 1958,
        'genre': 'Roman',
        'taal': 'Nederlands',
        'pagina_aantal': 256
    }
    with patch('src.services.boekcreateservice.get_db', return_value=mock_db):
        service = BoekCreateService()
        with pytest.raises(BoekCreateException):
            service.create_boek(boek_data)

def test_create_boek_invalid_isbn_format():
    mock_db = MagicMock()
    boek_data = {
        'titel': 'De Avonden',
        'auteur': 'Gerard Reve',
        'isbn': 'ISBN-FOUT',
        'uitgever': 'De Bezige Bij',
        'publicatiejaar': 1947,
        'genre': 'Roman',
        'taal': 'Nederlands',
        'pagina_aantal': 400
    }
    with patch('src.services.boekcreateservice.get_db', return_value=mock_db):
        service = BoekCreateService()
        with pytest.raises(BoekCreateException):
            service.create_boek(boek_data)

def test_create_boek_duplicate_isbn():
    mock_db = MagicMock()
    boek_data = {
        'titel': 'Twee Gezichten',
        'auteur': 'Karel Glastra van Loon',
        'isbn': '9789023461212',
        'uitgever': 'De Arbeiderspers',
        'publicatiejaar': 2001,
        'genre': 'Thriller',
        'taal': 'Nederlands',
        'pagina_aantal': 285
    }
    mock_db.execute.side_effect = Exception("UNIQUE constraint failed: boeken.isbn")
    with patch('src.services.boekcreateservice.get_db', return_value=mock_db):
        service = BoekCreateService()
        with pytest.raises(BoekCreateException):
            service.create_boek(boek_data)

def test_create_boek_db_failure():
    mock_db = MagicMock()
    boek_data = {
        'titel': 'Het Diner',
        'auteur': 'Herman Koch',
        'isbn': '9789023454795',
        'uitgever': 'Ambo Anthos',
        'publicatiejaar': 2009,
        'genre': 'Roman',
        'taal': 'Nederlands',
        'pagina_aantal': 301
    }
    mock_db.execute.side_effect = Exception("Database connection lost")
    with patch('src.services.boekcreateservice.get_db', return_value=mock_db):
        service = BoekCreateService()
        with pytest.raises(BoekCreateException):
            service.create_boek(boek_data)