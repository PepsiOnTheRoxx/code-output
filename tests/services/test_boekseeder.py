import pytest
from unittest.mock import patch, MagicMock, call
from src.services.boekseeder import BoekSeeder, BoekService
from src.services.boekseeder_exceptions import BoekSeederException

def test_boekseeder_voegt_minimaal_vijf_boeken_toe():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch.object(BoekService, 'voeg_toe', autospec=True) as mock_voeg_toe:
        mock_service = BoekService()
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            seed.seed()
            assert mock_voeg_toe.call_count == 5
            for boek in dummy_boeken:
                mock_voeg_toe.assert_any_call(mock_service, boek)

def test_boekseeder_throwt_exception_als_service_faalt():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch.object(BoekService, 'voeg_toe', side_effect=Exception("Service failure"), autospec=True) as mock_voeg_toe:
        mock_service = BoekService()
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
    with patch.object(BoekService, 'voeg_toe', autospec=True) as mock_voeg_toe:
        mock_service = BoekService()
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
    with patch.object(BoekService, 'voeg_toe', autospec=True) as mock_voeg_toe:
        mock_service = BoekService()
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            try:
                seed.seed()
            except Exception as e:
                pytest.fail(f"Er mag geen exception gegooid worden bij succesvolle seed: {e}")

def test_boekseeder_geeft_juiste_calls_door_aan_boekservice():
    dummy_boeken = [
        {"titel": "Boek 1", "auteur": "Auteur 1"},
        {"titel": "Boek 2", "auteur": "Auteur 2"},
        {"titel": "Boek 3", "auteur": "Auteur 3"},
        {"titel": "Boek 4", "auteur": "Auteur 4"},
        {"titel": "Boek 5", "auteur": "Auteur 5"},
    ]
    with patch.object(BoekService, 'voeg_toe', autospec=True) as mock_voeg_toe:
        mock_service = BoekService()
        seed = BoekSeeder(mock_service)
        with patch.object(seed, '_maak_dummy_boeken', return_value=dummy_boeken):
            seed.seed()
            expected_calls = [call(mock_service, boek) for boek in dummy_boeken]
            mock_voeg_toe.assert_has_calls(expected_calls, any_order=False)
