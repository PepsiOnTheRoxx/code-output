import pytest
from unittest.mock import patch, MagicMock
from src.services.gebruikerdelete import GebruikerService
from src.services.gebruikerdelete_exceptions import GebruikerNotFoundException, GebruikerDeleteException

def test_gebruiker_verwijderen_succesvol():
    gebruiker_id = 42
    service = GebruikerService()
    with patch.object(service, '_vind_gebruiker', return_value=MagicMock()) as mock_vind, \
         patch.object(service, '_verwijder_gebruiker', return_value=None) as mock_verwijder:
        service.verwijder_gebruiker(gebruiker_id)
        mock_vind.assert_called_once_with(gebruiker_id)
        mock_verwijder.assert_called_once()

def test_gebruiker_verwijderen_bestaat_niet_raised():
    gebruiker_id = 101
    service = GebruikerService()
    with patch.object(service, '_vind_gebruiker', return_value=None):
        with pytest.raises(GebruikerNotFoundException):
            service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_operatie_faalt_raised():
    gebruiker_id = 55
    gebruiker_mock = MagicMock()
    service = GebruikerService()
    with patch.object(service, '_vind_gebruiker', return_value=gebruiker_mock), \
         patch.object(service, '_verwijder_gebruiker', side_effect=GebruikerDeleteException):
        with pytest.raises(GebruikerDeleteException):
            service.verwijder_gebruiker(gebruiker_id)

def test_gebruiker_verwijderen_met_foutieve_id_type():
    invalid_id = "niet_een_int"
    service = GebruikerService()
    with pytest.raises(TypeError):
        service.verwijder_gebruiker(invalid_id)

def test_gebruiker_verwijderen_roept_vind_gebruiker_op_met_juiste_id():
    gebruiker_id = 77
    service = GebruikerService()
    with patch.object(service, '_vind_gebruiker', return_value=MagicMock()) as mock_vind, \
         patch.object(service, '_verwijder_gebruiker', return_value=None):
        service.verwijder_gebruiker(gebruiker_id)
        mock_vind.assert_called_once_with(gebruiker_id)