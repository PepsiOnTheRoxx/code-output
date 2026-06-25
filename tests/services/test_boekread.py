import pytest
from unittest.mock import MagicMock, patch
from src.services.boekread import BoekReadService
from src.services.boekread_exceptions import BoekNietGevondenException, BoekDatabaseFoutException

@pytest.fixture
def mock_db_connection():
    return MagicMock()

def test_haal_alle_boeken_op_succesvol(mock_db_connection):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, "Titel1", "Auteur1"),
        (2, "Titel2", "Auteur2")
    ]
    mock_db_connection.cursor.return_value = mock_cursor

    service = BoekReadService(mock_db_connection)
    result = service.haal_alle_boeken_op()

    mock_db_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken"
    )
    assert result == [
        {'id': 1, 'titel': 'Titel1', 'auteur': 'Auteur1'},
        {'id': 2, 'titel': 'Titel2', 'auteur': 'Auteur2'}
    ]

def test_haal_alle_boeken_op_leeg_resultaat(mock_db_connection):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_db_connection.cursor.return_value = mock_cursor

    service = BoekReadService(mock_db_connection)
    result = service.haal_alle_boeken_op()

    assert result == []
    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken"
    )

def test_haal_boek_op_id_succesvol(mock_db_connection):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (3, "Titel3", "Auteur3")
    mock_db_connection.cursor.return_value = mock_cursor

    service = BoekReadService(mock_db_connection)
    result = service.haal_boek_op_id(3)

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken WHERE id = ?", (3,)
    )
    assert result == {'id': 3, 'titel': 'Titel3', 'auteur': 'Auteur3'}

def test_haal_boek_op_id_boek_niet_gevonden(mock_db_connection):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_db_connection.cursor.return_value = mock_cursor

    service = BoekReadService(mock_db_connection)
    with pytest.raises(BoekNietGevondenException):
        service.haal_boek_op_id(42)

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, titel, auteur FROM boeken WHERE id = ?", (42,)
    )

def test_haal_alle_boeken_op_database_fout(mock_db_connection):
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Database error")
    mock_db_connection.cursor.return_value = mock_cursor

    service = BoekReadService(mock_db_connection)
    with pytest.raises(BoekDatabaseFoutException):
        service.haal_alle_boeken_op()

def test_haal_boek_op_id_database_fout(mock_db_connection):
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Database error")
    mock_db_connection.cursor.return_value = mock_cursor

    service = BoekReadService(mock_db_connection)
    with pytest.raises(BoekDatabaseFoutException):
        service.haal_boek_op_id(1)
