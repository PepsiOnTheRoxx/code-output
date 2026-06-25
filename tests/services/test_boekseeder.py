import pytest
from unittest.mock import MagicMock, patch
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import DatabaseSeedError

@patch('src.services.boekseeder.db')
def test_seeder_inserts_minimaal_vijf_boeken(mock_db):
    mock_session = MagicMock()
    mock_db.session = mock_session
    mock_query = mock_session.query.return_value
    mock_query.count.return_value = 0  # Simuleer eerste opstart (leeg)
    seeder = BoekSeeder()
    seeder.seed()
    assert mock_session.add.call_count >= 5
    mock_session.commit.assert_called_once()

@patch('src.services.boekseeder.db')
def test_seeder_voegt_niet_opnieuw_toe_als_boeken_bestaan(mock_db):
    mock_session = MagicMock()
    mock_db.session = mock_session
    mock_query = mock_session.query.return_value
    mock_query.count.return_value = 5  # Simuleer boeken bestaan al
    seeder = BoekSeeder()
    seeder.seed()
    assert mock_session.add.call_count == 0
    mock_session.commit.assert_not_called()

@patch('src.services.boekseeder.db')
def test_seeder_rollback_bij_database_fout(mock_db):
    mock_session = MagicMock()
    mock_db.session = mock_session
    mock_query = mock_session.query.return_value
    mock_query.count.return_value = 0
    mock_session.commit.side_effect = Exception("Database error")
    seeder = BoekSeeder()
    with pytest.raises(DatabaseSeedError):
        seeder.seed()
    mock_session.rollback.assert_called_once()

@patch('src.services.boekseeder.db')
def test_seeder_raises_seederror_bij_commit_faalt(mock_db):
    mock_session = MagicMock()
    mock_db.session = mock_session
    mock_query = mock_session.query.return_value
    mock_query.count.return_value = 0
    mock_session.commit.side_effect = Exception("Commit faalt")
    seeder = BoekSeeder()
    with pytest.raises(DatabaseSeedError):
        seeder.seed()
    mock_session.rollback.assert_called_once()

@patch('src.services.boekseeder.db')
def test_seeder_seed_meerdere_malen_idempotent(mock_db):
    mock_session = MagicMock()
    mock_db.session = mock_session
    mock_query = mock_session.query.return_value

    # Eerste keer: geen boeken
    mock_query.count.return_value = 0
    seeder = BoekSeeder()
    seeder.seed()
    assert mock_session.add.call_count >= 5
    mock_session.commit.assert_called_once()
    mock_session.reset_mock()

    # Tweede keer: nu zijn er boeken
    mock_query.count.return_value = 5
    seeder.seed()
    assert mock_session.add.call_count == 0
    mock_session.commit.assert_not_called()