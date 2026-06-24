import pytest
from unittest.mock import MagicMock, patch
from src.services.creategebruiker import GebruikerService
from src.services.creategebruiker_exceptions import InvalidEmailException, DuplicateGebruikerException

@pytest.fixture
def gebruiker_repo_mock():
    with patch('src.services.creategebruiker.GebruikerRepository') as mock_repo:
        yield mock_repo.return_value

@pytest.fixture
def gebruiker_service(gebruiker_repo_mock):
    return GebruikerService(gebruiker_repo_mock)

def test_create_gebruiker_succesvol(gebruiker_service, gebruiker_repo_mock):
    gebruiker_repo_mock.exists_by_email.return_value = False
    gebruiker_repo_mock.save.return_value = MagicMock(id=1, naam="Jan Jansen", email="jan@voorbeeld.nl")
    result = gebruiker_service.create_gebruiker("Jan Jansen", "jan@voorbeeld.nl")
    assert result.naam == "Jan Jansen"
    assert result.email == "jan@voorbeeld.nl"
    gebruiker_repo_mock.save.assert_called_once()

def test_create_gebruiker_invalid_email(gebruiker_service):
    with pytest.raises(InvalidEmailException):
        gebruiker_service.create_gebruiker("Marieke de Groot", "foute-mail")

def test_create_gebruiker_duplicate_email(gebruiker_service, gebruiker_repo_mock):
    gebruiker_repo_mock.exists_by_email.return_value = True
    with pytest.raises(DuplicateGebruikerException):
        gebruiker_service.create_gebruiker("Piet Pieters", "piet@voorbeeld.nl")

def test_create_gebruiker_leeg_naam(gebruiker_service):
    with pytest.raises(ValueError):
        gebruiker_service.create_gebruiker("", "klaas@voorbeeld.nl")

def test_create_gebruiker_leeg_email(gebruiker_service):
    with pytest.raises(InvalidEmailException):
        gebruiker_service.create_gebruiker("Klaas van Dijk", "")