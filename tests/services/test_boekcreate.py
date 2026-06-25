import pytest
from unittest.mock import MagicMock
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekCreateDuplicateException, BoekCreateDatabaseException

@pytest.fixture
def db_connection():
    return MagicMock()

@pytest.fixture
def boek_data():
    return {
        "isbn": "978-1234567890",
        "titel": "Testtitel",
        "auteur": "Auteurnaam",
        "uitgever": "Uitgevernaam",
        "uitgiftejaar": 2020,
        "genre": "Fictie",
        "taal": "Nederlands",
        "pagina_aantal": 320,
        "beschrijving": "Omschrijving van het boek"
    }

def test_boek_create_success(db_connection, boek_data):
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.rowcount = 1

    service = BoekService(db_connection)
    service.create_boek(**boek_data)

    db_connection.cursor.assert_called_once()
    # Check existence-query
    mock_cursor.execute.assert_any_call(
        "SELECT 1 FROM boeken WHERE isbn = ?", (boek_data["isbn"],)
    )
    # Check insert-query
    mock_cursor.execute.assert_any_call(
        "INSERT INTO boeken (isbn, titel, auteur, uitgever, uitgiftejaar, genre, taal, pagina_aantal, beschrijving) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            boek_data["isbn"],
            boek_data["titel"],
            boek_data["auteur"],
            boek_data["uitgever"],
            boek_data["uitgiftejaar"],
            boek_data["genre"],
            boek_data["taal"],
            boek_data["pagina_aantal"],
            boek_data["beschrijving"],
        )
    )
    db_connection.commit.assert_called_once()

def test_boek_create_duplicate_raises_exception(db_connection, boek_data):
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)  # Boek bestaat al

    service = BoekService(db_connection)
    with pytest.raises(BoekCreateDuplicateException):
        service.create_boek(**boek_data)

    mock_cursor.execute.assert_called_with(
        "SELECT 1 FROM boeken WHERE isbn = ?", (boek_data["isbn"],)
    )
    db_connection.commit.assert_not_called()

def test_boek_create_db_error_raises_exception(db_connection, boek_data):
    mock_cursor = MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.execute.side_effect = [None, Exception("DB insert error")]

    service = BoekService(db_connection)
    with pytest.raises(BoekCreateDatabaseException):
        service.create_boek(**boek_data)

    db_connection.commit.assert_not_called()

def test_boek_create_incomplete_data_raises_exception(db_connection, boek_data):
    del boek_data["isbn"]
    service = BoekService(db_connection)
    with pytest.raises(TypeError):
        service.create_boek(**boek_data)
