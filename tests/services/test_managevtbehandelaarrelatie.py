import pytest
from unittest.mock import MagicMock, patch
from src.services.managevtbehandelaarrelatie import VTBehandelaarRelatieService
from src.services.managevtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieBestaatAlException,
    VTBehandelaarRelatieNietGevondenException,
    OngeldigeBehandelaarException,
)

@pytest.fixture
def service():
    return VTBehandelaarRelatieService()

def test_voeg_behandelaar_toe_succesvol(service):
    gebruiker_id = 1
    vernietigingstaak_id = 20
    with patch.object(service, "voeg_behandelaar_toe", return_value=True) as mock_method:
        result = service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)
        assert result is True
        mock_method.assert_called_once_with(gebruiker_id, vernietigingstaak_id)

def test_voeg_behandelaar_toe_bestaat_al_exception(service):
    gebruiker_id = 1
    vernietigingstaak_id = 20
    with patch.object(service, "voeg_behandelaar_toe", side_effect=VTBehandelaarRelatieBestaatAlException):
        with pytest.raises(VTBehandelaarRelatieBestaatAlException):
            service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)

def test_voeg_behandelaar_toe_ongeldige_behandelaar_exception(service):
    gebruiker_id = 99
    vernietigingstaak_id = 21
    with patch.object(service, "voeg_behandelaar_toe", side_effect=OngeldigeBehandelaarException):
        with pytest.raises(OngeldigeBehandelaarException):
            service.voeg_behandelaar_toe(gebruiker_id, vernietigingstaak_id)

def test_verwijder_behandelaar_succesvol(service):
    gebruiker_id = 2
    vernietigingstaak_id = 15
    with patch.object(service, "verwijder_behandelaar", return_value=True) as mock_method:
        result = service.verwijder_behandelaar(gebruiker_id, vernietigingstaak_id)
        assert result is True
        mock_method.assert_called_once_with(gebruiker_id, vernietigingstaak_id)

def test_verwijder_behandelaar_niet_gevonden_exception(service):
    gebruiker_id = 3
    vernietigingstaak_id = 18
    with patch.object(service, "verwijder_behandelaar", side_effect=VTBehandelaarRelatieNietGevondenException):
        with pytest.raises(VTBehandelaarRelatieNietGevondenException):
            service.verwijder_behandelaar(gebruiker_id, vernietigingstaak_id)

def test_get_behandelaars_by_taak_succesvol(service):
    vernietigingstaak_id = 40
    behandelaars = [10, 11, 12]
    with patch.object(service, "get_behandelaars_by_taak", return_value=behandelaars) as mock_method:
        result = service.get_behandelaars_by_taak(vernietigingstaak_id)
        assert result == behandelaars
        mock_method.assert_called_once_with(vernietigingstaak_id)

def test_get_taken_by_behandelaar_succesvol(service):
    gebruiker_id = 4
    taken = [100, 101]
    with patch.object(service, "get_taken_by_behandelaar", return_value=taken) as mock_method:
        result = service.get_taken_by_behandelaar(gebruiker_id)
        assert result == taken
        mock_method.assert_called_once_with(gebruiker_id)

def test_get_behandelaars_by_taak_geen_behandelaars(service):
    vernietigingstaak_id = 41
    with patch.object(service, "get_behandelaars_by_taak", return_value=[]) as mock_method:
        result = service.get_behandelaars_by_taak(vernietigingstaak_id)
        assert result == []
        mock_method.assert_called_once_with(vernietigingstaak_id)