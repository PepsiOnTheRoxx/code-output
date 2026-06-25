import pytest
from unittest.mock import MagicMock, patch
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekAlreadyExistsException, InvalidBoekDataException

@pytest.fixture
def mock_db():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

def test_create_boek_success(mock_db):
    mock_conn, mock_cursor = mock_db
    service = BoekService(db_connection=mock_conn)
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '978-1234567890',
        'publicatiejaar': 2022,
        'uitgever': 'Uitgeverij X',
        'pagina_teller': 200,
        'genre': 'Fictie',
        'taal': 'Nederlands'
    }
    mock_cursor.fetchone.return_value = None
    service.create_boek(**boek_data)
    insert_sql = (
        "INSERT INTO boek (titel, auteur, isbn, publicatiejaar, uitgever, pagina_teller, genre, taal) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    mock_cursor.execute.assert_any_call(
        "SELECT 1 FROM boek WHERE isbn=?",
        (boek_data['isbn'],)
    )
    mock_cursor.execute.assert_any_call(
        insert_sql,
        (
            boek_data['titel'],
            boek_data['auteur'],
            boek_data['isbn'],
            boek_data['publicatiejaar'],
            boek_data['uitgever'],
            boek_data['pagina_teller'],
            boek_data['genre'],
            boek_data['taal'],
        )
    )
    assert mock_conn.commit.called

def test_create_boek_already_exists(mock_db):
    mock_conn, mock_cursor = mock_db
    service = BoekService(db_connection=mock_conn)
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '978-1234567890',
        'publicatiejaar': 2022,
        'uitgever': 'Uitgeverij X',
        'pagina_teller': 200,
        'genre': 'Fictie',
        'taal': 'Nederlands'
    }
    mock_cursor.fetchone.return_value = (1,)
    with pytest.raises(BoekAlreadyExistsException):
        service.create_boek(**boek_data)
    mock_cursor.execute.assert_any_call(
        "SELECT 1 FROM boek WHERE isbn=?",
        (boek_data['isbn'],)
    )
    assert not mock_conn.commit.called

def test_create_boek_invalid_data_missing_attribute(mock_db):
    mock_conn, mock_cursor = mock_db
    service = BoekService(db_connection=mock_conn)
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '978-1234567890',
        # 'publicatiejaar' mist
        'uitgever': 'Uitgeverij X',
        'pagina_teller': 200,
        'genre': 'Fictie',
        'taal': 'Nederlands'
    }
    with pytest.raises(InvalidBoekDataException):
        service.create_boek(**boek_data)
    assert not mock_conn.commit.called

def test_create_boek_invalid_data_wrong_type(mock_db):
    mock_conn, mock_cursor = mock_db
    service = BoekService(db_connection=mock_conn)
    boek_data = {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '978-1234567890',
        'publicatiejaar': 'tweeduizendtweeëntwintig',  # verkeerde type
        'uitgever': 'Uitgeverij X',
        'pagina_teller': 200,
        'genre': 'Fictie',
        'taal': 'Nederlands'
    }
    with pytest.raises(InvalidBoekDataException):
        service.create_boek(**boek_data)
    assert not mock_conn.commit.called