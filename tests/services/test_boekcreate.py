import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekCreateDuplicateISBNException, BoekCreateInvalidDataException, BoekCreateDatabaseException

def valid_boek_data():
    return {
        "auteur": "J.K. Rowling",
        "beschrijving": "Een magisch avontuur",
        "is_uitgeleend": False,
        "isbn": "1234567890",
        "kaft_foto_url": "https://example.com/kaft.jpg",
        "publicatiedatum": date(1997, 6, 26),
        "titel": "Harry Potter en de Steen der Wijzen",
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_success(mock_repo_cls):
    boek_data = valid_boek_data()
    mock_repo = MagicMock()
    mock_repo.create.return_value = boek_data  # Simulatie van het aangemaakte boek
    mock_repo.exists.return_value = False
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    result = service.create_boek(**boek_data)

    assert result == boek_data
    mock_repo.exists.assert_called_once_with(isbn=boek_data["isbn"])
    mock_repo.create.assert_called_once_with({k: v for k, v in boek_data.items() if v is not None})

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_already_exists(mock_repo_cls):
    boek_data = valid_boek_data()
    mock_repo = MagicMock()
    mock_repo.exists.return_value = True
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    with pytest.raises(BoekCreateDuplicateISBNException):
        service.create_boek(**boek_data)
    mock_repo.exists.assert_called_once_with(isbn=boek_data["isbn"])
    mock_repo.create.assert_not_called()

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_invalid_data_missing_titel(mock_repo_cls):
    boek_data = valid_boek_data()
    boek_data.pop("titel")
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    with pytest.raises(BoekCreateInvalidDataException):
        service.create_boek(**boek_data)
    mock_repo.exists.assert_not_called()
    mock_repo.create.assert_not_called()

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_invalid_data_empty_isbn(mock_repo_cls):
    boek_data = valid_boek_data()
    boek_data["isbn"] = ""
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    with pytest.raises(BoekCreateInvalidDataException):
        service.create_boek(**boek_data)
    mock_repo.exists.assert_not_called()
    mock_repo.create.assert_not_called()

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_db_exception_on_create(mock_repo_cls):
    boek_data = valid_boek_data()
    mock_repo = MagicMock()
    mock_repo.exists.return_value = False
    mock_repo.create.side_effect = BoekCreateDatabaseException("Fout bij aanmaken boek")
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    with pytest.raises(BoekCreateDatabaseException):
        service.create_boek(**boek_data)
    mock_repo.exists.assert_called_once_with(isbn=boek_data["isbn"])
    mock_repo.create.assert_called_once_with({k: v for k, v in boek_data.items() if v is not None})

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_defaults_uitgeleend_niet_verplicht(mock_repo_cls):
    boek_data = valid_boek_data()
    boek_data.pop("uitgeleend_datum")
    boek_data.pop("uitgeleend_max_tot")
    expected_data = {k: v for k, v in boek_data.items() if v is not None}
    mock_repo = MagicMock()
    mock_repo.create.return_value = boek_data
    mock_repo.exists.return_value = False
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    result = service.create_boek(**boek_data)

    assert result == boek_data
    mock_repo.exists.assert_called_once_with(isbn=boek_data["isbn"])
    mock_repo.create.assert_called_once_with(expected_data)

@patch("src.services.boekcreate.BoekRepository")
def test_create_boek_with_publicatiedatum_none(mock_repo_cls):
    boek_data = valid_boek_data()
    boek_data["publicatiedatum"] = None
    expected_data = {k: v for k, v in boek_data.items() if v is not None}
    mock_repo = MagicMock()
    mock_repo.create.return_value = boek_data
    mock_repo.exists.return_value = False
    mock_repo_cls.return_value = mock_repo

    service = BoekService()
    result = service.create_boek(**boek_data)

    assert result == boek_data
    mock_repo.exists.assert_called_once_with(isbn=boek_data["isbn"])
    mock_repo.create.assert_called_once_with(expected_data)
