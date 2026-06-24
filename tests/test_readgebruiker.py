import pytest
from src.readgebruiker import GebruikerService
from src.readgebruiker_exceptions import GebruikerNietGevondenException, OngeldigeGebruikerIDException
from unittest.mock import Mock

def test_read_gebruiker_success():
    gebruiker_data = {'id': 1, 'naam': 'Jan Jansen', 'email': 'jan@domein.nl'}
    mock_repo = Mock()
    mock_repo.get_gebruiker_by_id.return_value = gebruiker_data
    service = GebruikerService(mock_repo)
    result = service.read_gebruiker(1)
    assert result['id'] == 1
    assert result['naam'] == 'Jan Jansen'
    assert result['email'] == 'jan@domein.nl'
    mock_repo.get_gebruiker_by_id.assert_called_once_with(1)

def test_read_gebruiker_not_found():
    mock_repo = Mock()
    mock_repo.get_gebruiker_by_id.return_value = None
    service = GebruikerService(mock_repo)
    with pytest.raises(GebruikerNietGevondenException):
        service.read_gebruiker(999)

def test_read_gebruiker_invalid_id_type():
    mock_repo = Mock()
    service = GebruikerService(mock_repo)
    with pytest.raises(OngeldigeGebruikerIDException):
        service.read_gebruiker('abc')

def test_read_gebruiker_missing_email():
    gebruiker_data = {'id': 2, 'naam': 'Els Example', 'email': None}
    mock_repo = Mock()
    mock_repo.get_gebruiker_by_id.return_value = gebruiker_data
    service = GebruikerService(mock_repo)
    result = service.read_gebruiker(2)
    assert result['id'] == 2
    assert result['naam'] == 'Els Example'
    assert result['email'] is None

def test_read_gebruiker_missing_naam():
    gebruiker_data = {'id': 3, 'naam': None, 'email': 'piet@voorbeeld.nl'}
    mock_repo = Mock()
    mock_repo.get_gebruiker_by_id.return_value = gebruiker_data
    service = GebruikerService(mock_repo)
    result = service.read_gebruiker(3)
    assert result['id'] == 3
    assert result['naam'] is None
    assert result['email'] == 'piet@voorbeeld.nl'

def test_read_gebruiker_with_additional_fields_ignored():
    gebruiker_data = {'id': 4, 'naam': 'Truus Test', 'email': 'truus@test.nl', 'rol': 'beheerder'}
    mock_repo = Mock()
    mock_repo.get_gebruiker_by_id.return_value = gebruiker_data
    service = GebruikerService(mock_repo)
    result = service.read_gebruiker(4)
    assert result['id'] == 4
    assert result['naam'] == 'Truus Test'
    assert result['email'] == 'truus@test.nl'
    assert 'rol' not in result
