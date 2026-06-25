import pytest
from unittest.mock import MagicMock
from src.services.seederdummyboeken import BoekSeeder
from src.services.seederdummyboeken_exceptions import BoekSeederAlreadySeededError, BoekSeederDatabaseError

def test_seeder_inserts_minimum_five_boeken():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None] * 6 # 1 SELECT + 5 INSERTS
    cursor.fetchone.return_value = (0,)

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    assert cursor.execute.call_count == 6
    insert_call = any("INSERT INTO boeken" in str(call[0][0]) for call in cursor.execute.call_args_list)
    assert insert_call
    db_connection.commit.assert_called_once()

def test_seeder_not_seed_if_already_seeded():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.return_value = None
    cursor.fetchone.return_value = (5,)

    seeder = BoekSeeder(db_connection)
    with pytest.raises(BoekSeederAlreadySeededError):
        seeder.seed()

def test_seeder_raises_databaseexception_on_failure():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("DB Error")

    seeder = BoekSeeder(db_connection)
    with pytest.raises(BoekSeederDatabaseError):
        seeder.seed()

def test_seeder_commit_called_after_insert():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None] * 6
    cursor.fetchone.return_value = (0,)

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    db_connection.commit.assert_called_once()

def test_seeder_executes_correct_select_query():
    db_connection = MagicMock()
    cursor = MagicMock()
    db_connection.cursor.return_value = cursor
    cursor.execute.side_effect = [None] * 6
    cursor.fetchone.return_value = (0,)

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
    cursor.execute.side_effect = [None] * 6
    cursor.fetchone.return_value = (0,)

    seeder = BoekSeeder(db_connection)
    seeder.seed()

    insert_called = any("INSERT INTO boeken" in call[0][0] for call in cursor.execute.call_args_list)
    assert insert_called
