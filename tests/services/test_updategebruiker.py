import pytest
from unittest.mock import patch, MagicMock
from src.services import updategebruiker
from src.services.updategebruiker_exceptions import GebruikerNietGevondenException, OnjuisteGebruikerDataException


@patch('src.services.updategebruiker.GebruikerRepository')
def test_update_gebruiker_success(mock_repository_class):
    mock_repository = MagicMock()
    mock_repository_class.return_value = mock_repository

    gebruiker_id = 1
    nieuwe_data = {'naam': 'Jan', 'email': 'jan@domein.nl'}
    bestaande_gebruiker = MagicMock()
    mock_repository.get_by_id.return_value = bestaande_gebruiker

    update_result = MagicMock()
    mock_repository.update.return_value = update_result

    result = updategebruiker.update_gebruiker(gebruiker_id, nieuwe_data)

    mock_repository.get_by_id.assert_called_once_with(gebruiker_id)
    mock_repository.update.assert_called_once_with(bestaande_gebruiker, nieuwe_data)
    assert result == update_result


@patch('src.services.updategebruiker.GebruikerRepository')
def test_update_gebruiker_gebruiker_niet_gevonden(mock_repository_class):
    mock_repository = MagicMock()
    mock_repository_class.return_value = mock_repository

    gebruiker_id = 99
    nieuwe_data = {'naam': 'Piet'}
    mock_repository.get_by_id.return_value = None

    with pytest.raises(GebruikerNietGevondenException):
        updategebruiker.update_gebruiker(gebruiker_id, nieuwe_data)

    mock_repository.get_by_id.assert_called_once_with(gebruiker_id)
    mock_repository.update.assert_not_called()


@patch('src.services.updategebruiker.GebruikerRepository')
def test_update_gebruiker_ongeldige_data(mock_repository_class):
    mock_repository = MagicMock()
    mock_repository_class.return_value = mock_repository

    gebruiker_id = 2
    bestaande_gebruiker = MagicMock()
    mock_repository.get_by_id.return_value = bestaande_gebruiker

    ongeldige_data = {'email': 'geen_email_formaat'}
    mock_repository.update.side_effect = OnjuisteGebruikerDataException("Ongeldig formaat")

    with pytest.raises(OnjuisteGebruikerDataException):
        updategebruiker.update_gebruiker(gebruiker_id, ongeldige_data)

    mock_repository.get_by_id.assert_called_once_with(gebruiker_id)
    mock_repository.update.assert_called_once_with(bestaande_gebruiker, ongeldige_data)


@patch('src.services.updategebruiker.GebruikerRepository')
def test_update_gebruiker_update_returnt_none(mock_repository_class):
    mock_repository = MagicMock()
    mock_repository_class.return_value = mock_repository

    gebruiker_id = 3
    nieuwe_data = {'naam': 'Tom'}
    bestaande_gebruiker = MagicMock()
    mock_repository.get_by_id.return_value = bestaande_gebruiker

    mock_repository.update.return_value = None

    result = updategebruiker.update_gebruiker(gebruiker_id, nieuwe_data)

    mock_repository.get_by_id.assert_called_once_with(gebruiker_id)
    mock_repository.update.assert_called_once_with(bestaande_gebruiker, nieuwe_data)
    assert result is None
