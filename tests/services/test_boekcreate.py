import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from src.services.boekcreate import BoekService
from src.services.boekcreate_exceptions import BoekAlreadyExistsException, InvalidBoekDataException


def test_create_boek_successful():
    boek_data = {
        "auteur": "J.K. Rowling",
        "beschrijving": "Fantasy boek",
        "isbn": "9781234567890",
        "publicatiedatum": date(2001, 11, 14),
        "kaft_foto_url": "http://example.com/hp.jpg",
        "is_uitgeleend": False,
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }
    mock_repo = MagicMock()
    mock_repo.exists.return_value = False
    mock_repo.create.return_value = 99
    service = BoekService(repo=mock_repo)
    result = service.create_boek(**boek_data)
    mock_repo.create.assert_called_once_with(
        auteur="J.K. Rowling",
        beschrijving="Fantasy boek",
        isbn="9781234567890",
        publicatiedatum=date(2001, 11, 14),
        kaft_foto_url="http://example.com/hp.jpg",
        is_uitgeleend=False,
        uitgeleend_datum=None,
        uitgeleend_max_tot=None
    )
    assert result == 99


def test_create_boek_already_exists_exception():
    boek_data = {
        "auteur": "J.K. Rowling",
        "beschrijving": "Fantasy boek",
        "isbn": "9781234567890",
        "publicatiedatum": date(2001, 11, 14),
        "kaft_foto_url": "http://example.com/hp.jpg",
        "is_uitgeleend": False,
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }
    mock_repo = MagicMock()
    mock_repo.exists.return_value = True
    service = BoekService(repo=mock_repo)
    with pytest.raises(BoekAlreadyExistsException):
        service.create_boek(**boek_data)


def test_create_boek_invalid_data_exception():
    boek_data = {
        "auteur": "",
        "beschrijving": "Slecht boek",
        "isbn": "invalideisbn",  # Onjuist ISBN-formaat
        "publicatiedatum": "onjuistedatum",
        "kaft_foto_url": "http://example.com/boek.jpg",
        "is_uitgeleend": False,
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }
    mock_repo = MagicMock()
    service = BoekService(repo=mock_repo)
    with pytest.raises(InvalidBoekDataException):
        service.create_boek(**boek_data)


def test_create_boek_defaults_correctly_when_fields_missing():
    boek_data = {
        "auteur": "Auteur A",
        "beschrijving": "Beschrijving",
        "isbn": "9781111111111",
        "publicatiedatum": date(2020, 1, 1),
        "kaft_foto_url": None,
        "is_uitgeleend": False,
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }
    mock_repo = MagicMock()
    mock_repo.exists.return_value = False
    service = BoekService(repo=mock_repo)
    service.create_boek(**boek_data)
    mock_repo.create.assert_called_once_with(
        auteur="Auteur A",
        beschrijving="Beschrijving",
        isbn="9781111111111",
        publicatiedatum=date(2020, 1, 1),
        kaft_foto_url=None,
        is_uitgeleend=False,
        uitgeleend_datum=None,
        uitgeleend_max_tot=None
    )


def test_create_boek_passes_boolean_correctly():
    boek_data = {
        "auteur": "Auteursnaam",
        "beschrijving": "boekbeschrijving",
        "isbn": "9789999999999",
        "publicatiedatum": date(2023, 7, 21),
        "kaft_foto_url": "http://foto.url",
        "is_uitgeleend": True,
        "uitgeleend_datum": date(2024, 1, 1),
        "uitgeleend_max_tot": date(2024, 2, 1)
    }
    mock_repo = MagicMock()
    mock_repo.exists.return_value = False
    mock_repo.create.return_value = 21
    service = BoekService(repo=mock_repo)
    result = service.create_boek(**boek_data)
    mock_repo.create.assert_called_once_with(
        auteur="Auteursnaam",
        beschrijving="boekbeschrijving",
        isbn="9789999999999",
        publicatiedatum=date(2023, 7, 21),
        kaft_foto_url="http://foto.url",
        is_uitgeleend=True,
        uitgeleend_datum=date(2024, 1, 1),
        uitgeleend_max_tot=date(2024, 2, 1)
    )
    assert result == 21
