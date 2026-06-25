import pytest
from unittest.mock import MagicMock, patch
from database import DatabaseSetup, get_boek_columns, CREATE_BOEK_TABLE
from database_exceptions import DatabaseInitializationError

def test_init_creates_boek_table():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    db_setup = DatabaseSetup(mock_conn)
    db_setup.initialize_database()

    mock_cursor.execute.assert_any_call(CREATE_BOEK_TABLE)
    mock_conn.commit.assert_called_once()

    # Controleren of get_boek_columns de juiste velden teruggeeft
    assert get_boek_columns() == [
        'id', 'titel', 'auteur', 'isbn', 'uitgever',
        'jaar', 'categorie', 'taal', 'pagina_count', 'samenvatting'
    ]

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

# Nieuwe test: Consistentie van het Boek-table schema -- werkt in memory
import sqlite3

def test_boek_table_schema_is_consistent():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(CREATE_BOEK_TABLE)

    cursor.execute("PRAGMA table_info(Boek)")
    cols = [row[1] for row in cursor.fetchall()]
    assert cols == get_boek_columns()
    conn.close()