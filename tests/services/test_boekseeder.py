import pytest
from unittest.mock import MagicMock, patch
from src.services.boekseeder import BoekSeeder
from src.services.boekseeder_exceptions import BoekSeederException

@pytest.fixture
def boekservice_mock():
    return MagicMock()

def test_boekseeder_voegt_minimaal_5_boeken_toe(boekservice_mock):
    seeder = BoekSeeder(boekservice_mock)
    seeder.seed()
    assert boekservice_mock.voeg_toe.call_count >= 5
    for call in boekservice_mock.voeg_toe.call_args_list:
        boek_data = call.args[0]
        assert isinstance(boek_data, dict)
        assert 'auteur' in boek_data
        assert 'beschrijving' in boek_data
        assert 'isbn' in boek_data
        assert 'publicatiedatum' in boek_data
        assert 'kaft_foto_url' in boek_data
        assert 'is_uitgeleend' in boek_data
        assert 'uitgeleend_datum' in boek_data
        assert 'uitgeleend_max_tot' in boek_data

def test_boekseeder_roept_boekservice_met_juiste_argumenten(boekservice_mock):
    seeder = BoekSeeder(boekservice_mock)
    seeder.seed()
    for call in boekservice_mock.voeg_toe.call_args_list:
        boek = call.args[0]
        assert type(boek['auteur']) == str
        assert type(boek['beschrijving']) == str
        assert type(boek['isbn']) == str
        assert boek['publicatiedatum'] is None or type(boek['publicatiedatum']).__name__ in ('date', 'str')
        assert type(boek['kaft_foto_url']) == str
        assert type(boek['is_uitgeleend']) == bool
        assert boek['uitgeleend_datum'] is None or type(boek['uitgeleend_datum']).__name__ in ('date', 'str')
        assert boek['uitgeleend_max_tot'] is None or type(boek['uitgeleend_max_tot']).__name__ in ('date', 'str')

def test_boekseeder_exception_handling_bij_boekservice_fout(boekservice_mock):
    boekservice_mock.voeg_toe.side_effect = Exception("Database fout")
    seeder = BoekSeeder(boekservice_mock)
    with pytest.raises(BoekSeederException):
        seeder.seed()

def test_boekseeder_multiple_seeds_voegt_opnieuw_boeken_toe(boekservice_mock):
    seeder = BoekSeeder(boekservice_mock)
    seeder.seed()
    call_count_1 = boekservice_mock.voeg_toe.call_count
    seeder.seed()
    call_count_2 = boekservice_mock.voeg_toe.call_count
    assert call_count_2 >= call_count_1 * 2

def test_boekseeder_seed_mislukt_niets_toegevoegd(boekservice_mock):
    boekservice_mock.voeg_toe.side_effect = Exception("Fout tijdens toevoegen")
    seeder = BoekSeeder(boekservice_mock)
    with pytest.raises(BoekSeederException):
        seeder.seed()
    # Controle: alle calls zijn gefaald door exception; boekservice is nog steeds aangeroepen
    assert boekservice_mock.voeg_toe.call_count >= 1