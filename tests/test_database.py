import pytest
from unittest.mock import MagicMock, patch
from database import DatabaseSetup
from database_exceptions import DatabaseInitializationError

def test_init_creates_boek_table():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    db_setup = DatabaseSetup(mock_conn)
    db_setup.initialize_database()

    create_table_query = (
        "CREATE TABLE IF NOT EXISTS Boek "
        "("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "titel TEXT, "
        "auteur TEXT, "
        "isbn TEXT, "
        "uitgever TEXT, "
        "jaar INTEGER, "
        "categorie TEXT, "
        "taal TEXT, "
        "pagina_count INTEGER, "
        "samenvatting TEXT"
        ")"
    )
    mock_cursor.execute.assert_any_call(create_table_query)
    mock_conn.commit.assert_called_once()

def test_init_database_raises_on_db_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL error")

    db_setup = DatabaseSetup(mock_conn)
    with pytest.raises(DatabaseInitializationError):
        db_setup.initialize_database()

def test_commit_not_called_on_failure():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("SQL error")

    db_setup = DatabaseSetup(mock_conn)
    with pytest.raises(DatabaseInitializationError):
        db_setup.initialize_database()
    mock_conn.commit.assert_not_called()