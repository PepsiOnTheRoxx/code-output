import pytest
from unittest.mock import patch, MagicMock
from src.services.boekseederservice import BoekSeeder
from src.services.boekseederservice_exceptions import DatabaseInitialisatieFout

@pytest.fixture
def dummy_boeken():
    return [
        {"titel": "Boek 1", "auteur": "Auteur 1", "isbn": "ISBN1", "jaar": 2001},
        {"titel": "Boek 2", "auteur": "Auteur 2", "isbn": "ISBN2", "jaar": 2002},
        {"titel": "Boek 3", "auteur": "Auteur 3", "isbn": "ISBN3", "jaar": 2003},
        {"titel": "Boek 4", "auteur": "Auteur 4", "isbn": "ISBN4", "jaar": 2004},
        {"titel": "Boek 5", "auteur": "Auteur 5", "isbn": "ISBN5", "jaar": 2005},
    ]

def test_init_creates_database_if_not_exists():
    with patch('src.services.boekseederservice.sqlite3.connect') as mock_connect:
        conn_mock = MagicMock()
        mock_connect.return_value = conn_mock
        seeder = BoekSeeder()
        seeder.initialiseer_database()
        mock_connect.assert_called_once()
        assert conn_mock.cursor.return_value.execute.called
        assert conn_mock.commit.called
        assert conn_mock.close.called

def test_database_initialisatie_fout_bij_sqlite_error():
    with patch('src.services.boekseederservice.sqlite3.connect', side_effect=Exception("Fout")):
        seeder = BoekSeeder()
        with pytest.raises(DatabaseInitialisatieFout):
            seeder.initialiseer_database()

def test_seederen_insert_5_dummy_boeken(dummy_boeken):
    with patch('src.services.boekseederservice.sqlite3.connect') as mock_connect, \
         patch('src.services.boekseederservice.BoekSeeder._genereer_dummy_boeken', return_value=dummy_boeken):

        conn_mock = MagicMock()
        cursor_mock = MagicMock()
        conn_mock.cursor.return_value = cursor_mock
        mock_connect.return_value = conn_mock
        seeder = BoekSeeder()
        seeder.seed()
        assert cursor_mock.executemany.call_count == 1
        assert "INSERT INTO boeken" in cursor_mock.executemany.call_args[0][0]
        assert len(cursor_mock.executemany.call_args[0][1]) == 5
        assert conn_mock.commit.called
        assert conn_mock.close.called

def test_seederen_doe_niet_opnieuw_als_al_gegevens(dummy_boeken):
    with patch('src.services.boekseederservice.sqlite3.connect') as mock_connect:
        conn_mock = MagicMock()
        cursor_mock = MagicMock()
        cursor_mock.fetchone.return_value = (5,)
        conn_mock.cursor.return_value = cursor_mock
        mock_connect.return_value = conn_mock
        seeder = BoekSeeder()
        with patch.object(seeder, "_genereer_dummy_boeken") as mock_gen_boek:
            seeder.seed()
            mock_gen_boek.assert_not_called()
            assert not cursor_mock.executemany.called

def test_seederen_raise_fout_bij_exception():
    with patch('src.services.boekseederservice.sqlite3.connect') as mock_connect:
        conn_mock = MagicMock()
        cursor_mock = MagicMock()
        cursor_mock.execute.side_effect = Exception("DB error")
        conn_mock.cursor.return_value = cursor_mock
        mock_connect.return_value = conn_mock
        seeder = BoekSeeder()
        with pytest.raises(DatabaseInitialisatieFout):
            seeder.seed()