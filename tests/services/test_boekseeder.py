import pytest
from unittest.mock import MagicMock, patch, call
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import DatabaseSetupException, DummyDataInsertException

def test_boekseeder_create_tables_and_insert_dummy_books_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.return_value = None
    mock_cursor.fetchall.side_effect = [
        [],  # No tables exist initially
    ]
    mock_cursor.rowcount = 1

    seeder = BoekSeeder(mock_conn)
    seeder.seed()

    # Controle op tabellen-check en creatie
    mock_cursor.execute.assert_any_call(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='boeken';"
    )
    mock_cursor.execute.assert_any_call(
        "CREATE TABLE IF NOT EXISTS boeken (id INTEGER PRIMARY KEY AUTOINCREMENT, titel TEXT, auteur TEXT, jaar INTEGER);"
    )

    assert call(
        "INSERT INTO boeken (titel, auteur, jaar) VALUES (?, ?, ?);",
        ('Dummy Boek 1', 'Auteur 1', 2001)
    ) in mock_cursor.execute.call_args_list

def test_boekseeder_tables_already_exist_inserts_dummy_data():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    # 'boeken' table bestaat al
    mock_cursor.execute.side_effect = [
        None,  # table exists check
        None,  # count dummy boeken
        None,  # insert dummy boeken
    ]
    mock_cursor.fetchall.side_effect = [
        [('boeken',)],
        [(0,)],
    ]
    mock_cursor.rowcount = 1

    seeder = BoekSeeder(mock_conn)
    seeder.seed()

    assert call(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='boeken';"
    ) in mock_cursor.execute.call_args_list
    assert call(
        "SELECT COUNT(*) FROM boeken;"
    ) in mock_cursor.execute.call_args_list

    # Minimaal één dummy-insert moet zijn aangeroepen
    boek_calls = [
        c for c in mock_cursor.execute.call_args_list
        if c[0][0].startswith("INSERT INTO boeken")
    ]
    assert len(boek_calls) >= 5

def test_boekseeder_raises_on_database_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("DB Error")

    seeder = BoekSeeder(mock_conn)
    with pytest.raises(DatabaseSetupException):
        seeder.seed()

def test_boekseeder_raises_on_dummy_data_insert_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = [
        None,  # table exists check
        None,  # get count
        Exception("Insert error"),  # insert fails
    ]
    mock_cursor.fetchall.side_effect = [
        [],        # table bestaat niet
        [(0,)],   # geen rijen
    ]

    seeder = BoekSeeder(mock_conn)
    with pytest.raises(DummyDataInsertException):
        seeder.seed()

def test_boekseeder_does_not_insert_if_books_present():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = [
        None,  # table exists check
        None,  # get count
    ]
    mock_cursor.fetchall.side_effect = [
        [('boeken',)],  # tabel bestaat
        [(10,)],        # er zijn al 10 boeken
    ]

    seeder = BoekSeeder(mock_conn)
    seeder.seed()

    insert_calls = [
        c for c in mock_cursor.execute.call_args_list
        if c[0][0].startswith("INSERT INTO boeken")
    ]
    assert len(insert_calls) == 0