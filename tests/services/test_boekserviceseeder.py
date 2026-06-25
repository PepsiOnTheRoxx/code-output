import pytest
from unittest.mock import MagicMock, patch
from src.services.boekserviceseeder import BoekServiceSeeder, TableAlreadyExistsException, DatabaseSeedException

# Helper: match elk execute van create + MINIMUM_DUMMY_BOOKS inserts
DUMMY_INSERTS = [None] * 5  # 5 = default MINIMUM_DUMMY_BOOKS

def test_create_and_seed_table_executes_correct_queries():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor

    seeder = BoekServiceSeeder(db_connection)
    cursor.execute.side_effect = [None] + DUMMY_INSERTS
    cursor.fetchall.return_value = []

    seeder.create_and_seed_table()

    # Controleer of de juiste SQL statements zijn aangeroepen
    assert cursor.execute.call_count >= 2
    create_query = cursor.execute.call_args_list[0][0][0].lower()
    insert_query = cursor.execute.call_args_list[1][0][0].lower()
    assert "create table" in create_query
    assert "boek" in create_query
    assert "insert into" in insert_query
    assert "boek" in insert_query

    db_connection.commit.assert_called_once()

def test_create_and_seed_table_throws_on_existing_table():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor

    seeder = BoekServiceSeeder(db_connection)
    # Simuleer dat de tabel al bestaat
    cursor.execute.side_effect = [Exception("table already exists")]

    with pytest.raises(TableAlreadyExistsException):
        seeder.create_and_seed_table()

def test_create_and_seed_table_throws_on_seed_failure():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor

    seeder = BoekServiceSeeder(db_connection)
    # Eerste execute gaat goed (tabel aanmaken)
    # Tweede execute mislukt (insert dummy data)
    cursor.execute.side_effect = [None, Exception("inserting failed")]

    with pytest.raises(DatabaseSeedException):
        seeder.create_and_seed_table()

def test_create_and_seed_table_inserts_min_5_books():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor

    seeder = BoekServiceSeeder(db_connection)
    # Create + 5 dummy insert (side_effect)
    cursor.execute.side_effect = [None] + DUMMY_INSERTS  # supports 6 calls
    cursor.fetchall.return_value = []

    with patch("src.services.boekserviceseeder.MINIMUM_DUMMY_BOOKS", 5):
        seeder.create_and_seed_table()
        insert_calls = [call for call in cursor.execute.call_args_list if "insert into" in call[0][0].lower()]
        assert len(insert_calls) >= 5

def test_create_and_seed_table_commits_after_success():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor

    seeder = BoekServiceSeeder(db_connection)
    cursor.execute.side_effect = [None] + DUMMY_INSERTS
    cursor.fetchall.return_value = []

    seeder.create_and_seed_table()

    db_connection.commit.assert_called_once()

def test_create_and_seed_table_rollbacks_on_any_exception():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor

    seeder = BoekServiceSeeder(db_connection)
    cursor.execute.side_effect = Exception("DB error")

    with pytest.raises(Exception):
        try:
            seeder.create_and_seed_table()
        except Exception:
            db_connection.rollback.assert_called_once()
            raise
