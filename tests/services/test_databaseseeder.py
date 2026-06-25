import pytest
from unittest.mock import MagicMock, patch
from src.services.databaseseeder import DatabaseSeeder
from src.services.databaseseeder_exceptions import DatabaseSeedingError

@pytest.fixture
def mock_db_connection():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

def test_seeder_executes_inserts_and_commits_once(mock_db_connection):
    db_conn, mock_cursor = mock_db_connection
    db_seeder = DatabaseSeeder(db_conn)

    # Simuleer geen reeds bestaande boeken
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = (0,)

    db_seeder.seed_books()

    # Controleer de count(*) query
    expected_count_query = "SELECT COUNT(*) FROM books"
    mock_cursor.execute.assert_any_call(expected_count_query)
    # Controleer minimaal 5 insert statements
    insert_queries = [c[0][0] for c in mock_cursor.execute.call_args_list if "INSERT INTO books" in c[0][0]]
    assert len(insert_queries) >= 5
    # Controleer commit aangeroepen, maar geen rollback
    db_conn.commit.assert_called_once()
    db_conn.rollback.assert_not_called()

def test_seeder_overslaat_indien_reeds_boeken_aanwezig(mock_db_connection):
    db_conn, mock_cursor = mock_db_connection
    db_seeder = DatabaseSeeder(db_conn)
    # Simuleer dat er al boeken bestaan
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.return_value = (5,)

    db_seeder.seed_books()

    # Controleer dat geen INSERT is uitgevoerd
    executed_queries = [c[0][0] for c in mock_cursor.execute.call_args_list]
    assert any("SELECT COUNT(*) FROM books" in q for q in executed_queries)
    assert not any("INSERT INTO books" in q for q in executed_queries)
    db_conn.commit.assert_not_called()
    db_conn.rollback.assert_not_called()

def test_raise_exception_bij_database_fout(mock_db_connection):
    db_conn, mock_cursor = mock_db_connection
    db_seeder = DatabaseSeeder(db_conn)
    # Simuleer database fout bij execute
    mock_cursor.execute.side_effect = Exception("DB-fout")

    with pytest.raises(DatabaseSeedingError):
        db_seeder.seed_books()
    db_conn.rollback.assert_called_once()

def test_seeder_close_cursor_altijd(mock_db_connection):
    db_conn, mock_cursor = mock_db_connection
    db_seeder = DatabaseSeeder(db_conn)
    # Geen bestaande boeken om seeden af te dwingen
    mock_cursor.fetchone.return_value = (0,)

    try:
        db_seeder.seed_books()
    except Exception:
        pass
    assert mock_cursor.close.called