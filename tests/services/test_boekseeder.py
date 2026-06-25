import pytest
from unittest.mock import patch, MagicMock
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import BoekSeedingException

def test_run_seeds_at_least_five_records():
    dummy_boeken = [
        {"titel": "Boek 1"},
        {"titel": "Boek 2"},
        {"titel": "Boek 3"},
        {"titel": "Boek 4"},
        {"titel": "Boek 5"}
    ]
    with patch("src.services.boekseeder.BoekService") as MockBoekService:
        mock_service = MockBoekService.return_value
        mock_service.create.side_effect = [None]*5
        seeder = BoekSeeder()
        with patch("src.services.boekseeder.dummy_boeken", dummy_boeken):
            seeder.run()
        assert mock_service.create.call_count >= 5
        for call_arg in mock_service.create.call_args_list:
            assert isinstance(call_arg[0][0], dict)
            assert "titel" in call_arg[0][0]

def test_run_raises_exception_when_service_fails():
    with patch("src.services.boekseeder.BoekService") as MockBoekService:
        mock_service = MockBoekService.return_value
        mock_service.create.side_effect = Exception("Database error")
        seeder = BoekSeeder()
        with pytest.raises(BoekSeedingException) as exc:
            seeder.run()
        assert "Database error" in str(exc.value)

def test_run_calls_service_with_correct_data():
    dummy_boeken = [
        {"titel": "Testboek", "auteur": "Auteur X"},
        {"titel": "Testboek2", "auteur": "Auteur Y"},
        {"titel": "Testboek3", "auteur": "Auteur Z"},
        {"titel": "Testboek4", "auteur": "Auteur Q"},
        {"titel": "Testboek5", "auteur": "Auteur W"}
    ]
    with patch("src.services.boekseeder.BoekService") as MockBoekService:
        mock_service = MockBoekService.return_value
        mock_service.create = MagicMock()
        seeder = BoekSeeder()
        with patch("src.services.boekseeder.dummy_boeken", dummy_boeken):
            seeder.run()
        for idx, call in enumerate(mock_service.create.call_args_list):
            assert call[0][0]["titel"] == dummy_boeken[idx]["titel"]
            assert call[0][0]["auteur"] == dummy_boeken[idx]["auteur"]

def test_run_handles_partial_failure():
    dummy_boeken = [
        {"titel": f"Boek {i}"} for i in range(5)
    ]
    with patch("src.services.boekseeder.BoekService") as MockBoekService:
        mock_service = MockBoekService.return_value
        mock_service.create.side_effect = [None, Exception("DB Fout"), None, None, None]
        seeder = BoekSeeder()
        with patch("src.services.boekseeder.dummy_boeken", dummy_boeken):
            with pytest.raises(BoekSeedingException) as excinfo:
                seeder.run()
        assert "DB Fout" in str(excinfo.value)
        assert mock_service.create.call_count >= 2

def test_run_invokes_create_per_boek():
    dummy_boeken = [
        {"titel": f"Boek {i}"} for i in range(8)
    ]
    with patch("src.services.boekseeder.BoekService") as MockBoekService:
        mock_service = MockBoekService.return_value
        mock_service.create = MagicMock()
        seeder = BoekSeeder()
        with patch("src.services.boekseeder.dummy_boeken", dummy_boeken):
            seeder.run()
        assert mock_service.create.call_count == len(dummy_boeken)
