import pytest
from unittest.mock import patch, MagicMock
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import BoekSeederException

def test_boekseeder_voegt_vijf_of_meer_boeken_toe():
    mock_service = MagicMock()
    seeder = BoekSeeder(service=mock_service)
    seeder.seed()
    assert mock_service.voeg_boek_toe.call_count >= 5

def test_boekseeder_boek_data_juist_doorgegeven():
    mock_service = MagicMock()
    seeder = BoekSeeder(service=mock_service)
    seeder.seed()
    for call_args in mock_service.voeg_boek_toe.call_args_list:
        boek_data = call_args[0][0]
        assert isinstance(boek_data, dict)
        assert "titel" in boek_data
        assert "auteur" in boek_data

def test_boekseeder_raises_exception_bij_service_fout():
    mock_service = MagicMock()
    mock_service.voeg_boek_toe.side_effect = Exception("Fout in service")
    seeder = BoekSeeder(service=mock_service)
    with pytest.raises(BoekSeederException):
        seeder.seed()

def test_boekseeder_seed_herhaald_uitvoerbaar():
    mock_service = MagicMock()
    seeder = BoekSeeder(service=mock_service)
    seeder.seed()
    eerste_calls = mock_service.voeg_boek_toe.call_count
    seeder.seed()
    tweede_calls = mock_service.voeg_boek_toe.call_count
    assert eerste_calls == tweede_calls // 2

def test_boekseeder_seed_returntype_is_none():
    mock_service = MagicMock()
    seeder = BoekSeeder(service=mock_service)
    result = seeder.seed()
    assert result is None