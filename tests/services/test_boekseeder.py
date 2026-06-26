import pytest
from unittest.mock import patch, MagicMock
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import BoekSeederException

def test_boekseeder_voegt_minimaal_vijf_boeken_toe():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch('src.services.boekseeder.BoekService') as MockBoekService:
        mock_service = MockBoekService.return_value
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            seed.seed()
            calls = [pytest.call(boek) for boek in dummy_boeken]
            assert mock_service.voeg_toe.call_count == 5
            for boek in dummy_boeken:
                mock_service.voeg_toe.assert_any_call(boek)

def test_boekseeder_throwt_exception_als_service_faalt():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch('src.services.boekseeder.BoekService') as MockBoekService:
        mock_service = MockBoekService.return_value
        mock_service.voeg_toe.side_effect = Exception("Service failure")
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            with pytest.raises(BoekSeederException):
                seed.seed()

def test_boekseeder_geen_seed_als_minder_dan_vijf_boeken():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
    ]
    with patch('src.services.boekseeder.BoekService') as MockBoekService:
        mock_service = MockBoekService.return_value
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            with pytest.raises(BoekSeederException):
                seed.seed()

def test_boekseeder_successvolle_seed_geeft_geen_exception():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch('src.services.boekseeder.BoekService') as MockBoekService:
        mock_service = MockBoekService.return_value
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            try:
                seed.seed()
            except Exception:
                pytest.fail("Er mag geen exception gegooid worden bij succesvolle seed")

def test_boekseeder_geeft_juiste_calls_door_aan_boekservice():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch('src.services.boekseeder.BoekService') as MockBoekService:
        mock_service = MockBoekService.return_value
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            seed.seed()
            expected_calls = [pytest.call(boek) for boek in dummy_boeken]
            actual_calls = mock_service.voeg_toe.call_args_list
            for call, expected_call in zip(actual_calls, expected_calls):
                assert call == expected_call