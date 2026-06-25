import pytest
from unittest.mock import MagicMock
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekCreateAlreadyExistsException, BoekCreateDatabaseException

@pytest.fixture
def valid_boek_data():
    return {
        'titel': 'Test Boek',
        'auteur': 'Auteur Naam',
        'isbn': '1234567890',
        'publicatiejaar': 2023,
        'uitgeverij': 'Test Uitgever',
        'pagina_count': 300,
        'genre': 'Roman',
        'taal': 'Nederlands',
        'samenvatting': 'Samenvatting van het test boek.',
    }

@pytest.fixture
def mocked_db():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    return db_connection, cursor

def test_create_boek_success(mocked_db, valid_boek_data):
    db_connection, cursor = mocked_db
    cursor.fetchone.return_value = None
    cursor.rowcount = 1

    service = BoekService(db_connection)
    result = service.create(valid_boek_data)

    assert result is True
    db_connection.cursor.assert_called_once()
    cursor.execute.assert_any_call(
        "SELECT 1 FROM boek WHERE isbn = %s",
        (valid_boek_data['isbn'],)
    )
    cursor.execute.assert_any_call(
        "INSERT INTO boek (titel, auteur, isbn, publicatiejaar, uitgeverij, pagina_count, genre, taal, samenvatting)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            valid_boek_data['titel'],
            valid_boek_data['auteur'],
            valid_boek_data['isbn'],
            valid_boek_data['publicatiejaar'],
            valid_boek_data['uitgeverij'],
            valid_boek_data['pagina_count'],
            valid_boek_data['genre'],
            valid_boek_data['taal'],
            valid_boek_data['samenvatting'],
        )
    )
    db_connection.commit.assert_called_once()

def test_create_boek_already_exists(mocked_db, valid_boek_data):
    db_connection, cursor = mocked_db
    cursor.fetchone.return_value = (1,)

    service = BoekService(db_connection)
    with pytest.raises(BoekCreateAlreadyExistsException):
        service.create(valid_boek_data)

    cursor.execute.assert_called_with(
        "SELECT 1 FROM boek WHERE isbn = %s",
        (valid_boek_data['isbn'],)
    )
    db_connection.commit.assert_not_called()

def test_create_boek_insert_failed(mocked_db, valid_boek_data):
    db_connection, cursor = mocked_db
    cursor.fetchone.return_value = None
    cursor.rowcount = 0

    service = BoekService(db_connection)
    with pytest.raises(BoekCreateDatabaseException):
        service.create(valid_boek_data)

    cursor.execute.assert_any_call(
        "SELECT 1 FROM boek WHERE isbn = %s",
        (valid_boek_data['isbn'],)
    )
    cursor.execute.assert_any_call(
        "INSERT INTO boek (titel, auteur, isbn, publicatiejaar, uitgeverij, pagina_count, genre, taal, samenvatting)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            valid_boek_data['titel'],
            valid_boek_data['auteur'],
            valid_boek_data['isbn'],
            valid_boek_data['publicatiejaar'],
            valid_boek_data['uitgeverij'],
            valid_boek_data['pagina_count'],
            valid_boek_data['genre'],
            valid_boek_data['taal'],
            valid_boek_data['samenvatting'],
        )
    )
    db_connection.commit.assert_not_called()

def test_create_boek_rolls_back_on_insert_exception(mocked_db, valid_boek_data):
    db_connection, cursor = mocked_db
    cursor.fetchone.return_value = None
    cursor.execute.side_effect = [None, Exception("insert failed")]

    service = BoekService(db_connection)
    with pytest.raises(BoekCreateDatabaseException):
        service.create(valid_boek_data)

    db_connection.rollback.assert_called_once()
    db_connection.commit.assert_not_called()

def test_create_boek_rolls_back_on_commit_exception(mocked_db, valid_boek_data):
    db_connection, cursor = mocked_db
    cursor.fetchone.return_value = None
    cursor.rowcount = 1
    db_connection.commit.side_effect = Exception("DB commit failed")

    service = BoekService(db_connection)
    with pytest.raises(BoekCreateDatabaseException):
        service.create(valid_boek_data)

    db_connection.rollback.assert_called_once()
