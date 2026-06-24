import pytest
from unittest.mock import patch, MagicMock
from src.services.gebruikerupdate import GebruikerService, GebruikerRepository
from src.services.gebruikerupdate_exceptions import (
    GebruikerNietGevondenException,
    OngeldigeGebruikerUpdateException,
    DatabaseFoutException
)

@pytest.fixture
def mock_gebruiker():
    gebruiker = MagicMock()
    gebruiker.id = 1
    gebruiker.naam = 'Jan'
    gebruiker.email = 'jan@example.com'
    return gebruiker

@pytest.fixture
def service():
    # Handmatig repo in service zetten zodat patching werkt
    return GebruikerService()

@patch('src.services.gebruikerupdate.GebruikerRepository')
def test_update_gebruiker_succes(mock_repo_cls, service, mock_gebruiker):
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_gebruiker
    mock_repo.update.return_value = None
    mock_repo_cls.return_value = mock_repo
    # Forceer service.repo te refereren aan de gemockte repo
    service.repo = mock_repo
    
    update_data = {'naam': 'Piet', 'email': 'piet@example.com'}
    result = service.update_gebruiker(gebruiker_id=1, data=update_data)

    mock_repo.get_by_id.assert_called_once_with(1)
    assert mock_gebruiker.naam == 'Piet'
    assert mock_gebruiker.email == 'piet@example.com'
    mock_repo.update.assert_called_once_with(mock_gebruiker)
    assert result is True

@patch('src.services.gebruikerupdate.GebruikerRepository')
def test_update_gebruiker_niet_gevonden(mock_repo_cls, service):
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None
    mock_repo_cls.return_value = mock_repo
    service.repo = mock_repo

    with pytest.raises(GebruikerNietGevondenException):
        service.update_gebruiker(gebruiker_id=99, data={'naam': 'Onbekend'})

    mock_repo.get_by_id.assert_called_once_with(99)
    mock_repo.update.assert_not_called()

@patch('src.services.gebruikerupdate.GebruikerRepository')
def test_update_gebruiker_ongeldige_data(mock_repo_cls, service, mock_gebruiker):
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_gebruiker
    mock_repo_cls.return_value = mock_repo
    service.repo = mock_repo

    with pytest.raises(OngeldigeGebruikerUpdateException):
        service.update_gebruiker(gebruiker_id=1, data={'email': 'geen-at'})

    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_not_called()

@patch('src.services.gebruikerupdate.GebruikerRepository')
def test_update_gebruiker_db_fout(mock_repo_cls, service, mock_gebruiker):
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_gebruiker
    mock_repo.update.side_effect = DatabaseFoutException("Database niet bereikbaar")
    mock_repo_cls.return_value = mock_repo
    service.repo = mock_repo

    with pytest.raises(DatabaseFoutException):
        service.update_gebruiker(gebruiker_id=1, data={'naam': 'Klaas'})

    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_called_once_with(mock_gebruiker)
