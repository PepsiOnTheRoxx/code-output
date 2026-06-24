import pytest
from unittest.mock import patch, MagicMock
from src.services.vtproceseigenaarrelatie import VTProceseigenaarRelatieService
from src.services.vtproceseigenaarrelatie_exceptions import (
    GebruikerNotFoundException,
    TaakNotFoundException,
    RelatieAlreadyExistsException,
    RelatieNotFoundException
)

@pytest.fixture
def service():
    return VTProceseigenaarRelatieService()

def test_koppel_proceseigenaar_succesvol(service):
    gebruiker_id = 10
    taak_id = 20
    with patch.object(service, 'koppel_proceseigenaar') as mock_koppel:
        mock_koppel.return_value = True
        result = service.koppel_proceseigenaar(gebruiker_id, taak_id)
        assert result is True
        mock_koppel.assert_called_once_with(gebruiker_id, taak_id)

def test_koppel_proceseigenaar_gebruiker_bestaat_niet(service):
    gebruiker_id = 999
    taak_id = 20
    with patch.object(service, 'koppel_proceseigenaar', side_effect=GebruikerNotFoundException):
        with pytest.raises(GebruikerNotFoundException):
            service.koppel_proceseigenaar(gebruiker_id, taak_id)

def test_koppel_proceseigenaar_taak_bestaat_niet(service):
    gebruiker_id = 5
    taak_id = 12345
    with patch.object(service, 'koppel_proceseigenaar', side_effect=TaakNotFoundException):
        with pytest.raises(TaakNotFoundException):
            service.koppel_proceseigenaar(gebruiker_id, taak_id)

def test_koppel_proceseigenaar_reeds_gekoppeld(service):
    gebruiker_id = 12
    taak_id = 30
    with patch.object(service, 'koppel_proceseigenaar', side_effect=RelatieAlreadyExistsException):
        with pytest.raises(RelatieAlreadyExistsException):
            service.koppel_proceseigenaar(gebruiker_id, taak_id)

def test_verwijder_proceseigenaarrelatie_succesvol(service):
    gebruiker_id = 7
    taak_id = 33
    with patch.object(service, 'verwijder_proceseigenaarrelatie') as mock_verwijder:
        mock_verwijder.return_value = None
        service.verwijder_proceseigenaarrelatie(gebruiker_id, taak_id)
        mock_verwijder.assert_called_once_with(gebruiker_id, taak_id)

def test_verwijder_proceseigenaarrelatie_niet_gevonden(service):
    gebruiker_id = 99
    taak_id = 100
    with patch.object(service, 'verwijder_proceseigenaarrelatie', side_effect=RelatieNotFoundException):
        with pytest.raises(RelatieNotFoundException):
            service.verwijder_proceseigenaarrelatie(gebruiker_id, taak_id)

def test_get_proceseigenaren_voor_taak(service):
    taak_id = 50
    expected_proceseigenaren = [{'id': 1, 'naam': 'Piet'}, {'id': 2, 'naam': 'Klaas'}]
    with patch.object(service, 'get_proceseigenaren_voor_taak') as mock_get:
        mock_get.return_value = expected_proceseigenaren
        result = service.get_proceseigenaren_voor_taak(taak_id)
        assert result == expected_proceseigenaren
        mock_get.assert_called_once_with(taak_id)

def test_get_taken_voor_proceseigenaar(service):
    gebruiker_id = 25
    expected_taken = [{'id': 101, 'omschrijving': 'Taak A'}, {'id': 102, 'omschrijving': 'Taak B'}]
    with patch.object(service, 'get_taken_voor_proceseigenaar') as mock_get:
        mock_get.return_value = expected_taken
        result = service.get_taken_voor_proceseigenaar(gebruiker_id)
        assert result == expected_taken
        mock_get.assert_called_once_with(gebruiker_id)