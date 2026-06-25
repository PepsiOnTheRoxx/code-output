import pytest
from unittest.mock import MagicMock, patch
from src.services.seederdummyboeken import BoekSeeder
from src.services.seederdummyboeken_exceptions import AlreadySeededException, DatabaseException

def test_seeder_inserts_minimum_five_boeken():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None, None]
    cursor.fetchone.side_effect = [(0,), None]
    cursor.rowcount = 5

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    assert cursor.execute.call_count >= 2
    insert_call = any("INSERT INTO boeken" in str(call[0][0]) for call in cursor.execute.call_args_list)
    assert insert_call
    db_connection.commit.assert_called_once()

def test_seeder_not_seed_if_already_seeded():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None]
    cursor.fetchone.return_value = (5,)

    seeder = BoekSeeder(db_connection)
    with pytest.raises(AlreadySeededException):
        seeder.seed()

def test_seeder_raises_databaseexception_on_failure():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("DB Error")

    seeder = BoekSeeder(db_connection)
    with pytest.raises(DatabaseException):
        seeder.seed()

def test_seeder_commit_called_after_insert():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None, None]
    cursor.fetchone.side_effect = [(0,), None]
    cursor.rowcount = 5

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    db_connection.commit.assert_called_once()

def test_seeder_executes_correct_select_query():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None, None]
    cursor.fetchone.side_effect = [(0,), None]
    cursor.rowcount = 5

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    select_called = False
    for call in cursor.execute.call_args_list:
        if "SELECT COUNT(*) FROM boeken" in call[0][0]:
            select_called = True
    assert select_called

def test_seeder_executes_correct_insert_statement():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None, None]
    cursor.fetchone.side_effect = [(0,), None]
    cursor.rowcount = 5

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    insert_called = any("INSERT INTO boeken" in call[0][0] for call in cursor.execute.call_args_list)
    assert insert_called