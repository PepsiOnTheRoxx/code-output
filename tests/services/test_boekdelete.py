import pytest
from unittest.mock import patch, MagicMock
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNietGevondenException, BoekDeleteException

@pytest.fixture
def boek_service():
    return BoekService()

def test_verwijder_bestaand_boek_succesvol(boek_service):
    boek_id = 123
    with patch.object(boek_service, "haal_boek_op", return_value={"id": boek_id, "titel": "Testboek"}) as mock_haal_op, \
         patch.object(boek_service, "verwijder_boek_db", return_value=True) as mock_verwijder:
        resultaat = boek_service.verwijder_boek(boek_id)
        assert resultaat is True
        mock_haal_op.assert_called_once_with(boek_id)
        mock_verwijder.assert_called_once_with(boek_id)

def test_verwijder_boek_niet_gevonden(boek_service):
    boek_id = 124
    with patch.object(boek_service, "haal_boek_op", return_value=None):
        with pytest.raises(BoekNietGevondenException):
            boek_service.verwijder_boek(boek_id)

def test_verwijder_boek_db_faalt(boek_service):
    boek_id = 125
    with patch.object(boek_service, "haal_boek_op", return_value={"id": boek_id, "titel": "Foutiefboek"}), \
         patch.object(boek_service, "verwijder_boek_db", side_effect=BoekDeleteException("Fout bij verwijderen")):
        with pytest.raises(BoekDeleteException):
            boek_service.verwijder_boek(boek_id)

def test_verwijder_boek_onverwachte_exception(boek_service):
    boek_id = 126
    with patch.object(boek_service, "haal_boek_op", return_value={"id": boek_id, "titel": "Crashboek"}), \
         patch.object(boek_service, "verwijder_boek_db", side_effect=Exception("Onverwacht")):
        with pytest.raises(Exception) as exc:
            boek_service.verwijder_boek(boek_id)
        assert "Onverwacht" in str(exc.value)