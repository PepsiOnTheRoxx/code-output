import pytest
from unittest.mock import MagicMock, patch
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import BoekSeederDatabaseError


def test_seeder_voegt_minimaal_vijf_boeken_toe():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value = cursor
    cursor.rowcount = 5
    cursor.fetchone.return_value = None
    cursor.fetchall.return_value = []

    seeder = BoekSeeder(db_conn)
    seeder.seed()

    assert db_conn.cursor.called
    query = "INSERT INTO boeken"
    execute_calls = [call for call in cursor.execute.call_args_list if query in str(call)]
    assert len(execute_calls) >= 5
    assert db_conn.commit.called


def test_seeder_commit_wordt_aangeroepen():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value = cursor
    cursor.rowcount = 5

    seeder = BoekSeeder(db_conn)
    seeder.seed()

    assert db_conn.commit.called


def test_seeder_rollback_en_exception_bij_db_fout():
    db_conn = MagicMock()
    cursor = MagicMock()
    db_conn.cursor.return_value = cursor
    cursor.execute.side_effect = Exception("DB fout")

    seeder = BoekSeeder(db_conn)
    with pytest.raises(BoekSeederDatabaseError):
        seeder.seed()
    assert db_conn.rollback.called