import pytest
from unittest.mock import patch, MagicMock
from src.services.deletegebruiker import GebruikerService
from src.services.deletegebruiker_exceptions import GebruikerNietGevondenException, DeleteGebruikerException

def test_delete_gebruiker_success():
    gebruiker_id = 1
    service = GebruikerService()
    with patch.object(service.repository, 'gebruiker_bestaat', return_value=True), \
         patch.object(service.repository, 'verwijder_gebruiker', return_value=True):
        result = service.verwijder_gebruiker(gebruiker_id)
        assert result is True

def test_delete_gebruiker_not_found():
    gebruiker_id = 42
    service = GebruikerService()
    with patch.object(service.repository, 'gebruiker_bestaat', return_value=False):
        with pytest.raises(GebruikerNietGevondenException):
            service.verwijder_gebruiker(gebruiker_id)

def test_delete_gebruiker_database_error():
    gebruiker_id = 7
    service = GebruikerService()
    with patch.object(service.repository, 'gebruiker_bestaat', return_value=True), \
         patch.object(service.repository, 'verwijder_gebruiker', return_value=False):
        with pytest.raises(DeleteGebruikerException) as exc_info:
            service.verwijder_gebruiker(gebruiker_id)
        assert str(exc_info.value) == "Verwijderen van gebruiker is niet geslaagd."

def test_delete_gebruiker_calls_external_repository():
    gebruiker_id = 3
    with patch('src.services.deletegebruiker.GebruikerRepository') as mock_repo_cls:
        mock_repo_instance = MagicMock()
        mock_repo_cls.return_value = mock_repo_instance
        service = GebruikerService()
        # Patching gebruiker_bestaat to True and verwijder_gebruiker to True so no exceptions occur
        mock_repo_instance.gebruiker_bestaat.return_value = True
        mock_repo_instance.verwijder_gebruiker.return_value = True
        service.verwijder_gebruiker(gebruiker_id)
        assert mock_repo_cls.called
