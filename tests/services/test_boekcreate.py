import pytest
from unittest.mock import patch, MagicMock
from src.services.boekcreate import BoekService, BoekAlreadyExistsException
from src.services.boekcreate_exceptions import BoekCreateValidationException

@pytest.fixture
def boek_data():
    return {
        "titel": "De Ontdekking van de Hemel",
        "auteur": "Harry Mulisch",
        "isbn": "9789023431231",
        "jaar": 1992
    }

def test_create_boek_success(boek_data):
    with patch("src.services.boekcreate.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists.return_value = False
        mock_repo_instance.create.return_value = MagicMock(id=1, **boek_data)

        service = BoekService(repository=mock_repo_instance)
        result = service.create_boek(boek_data)

        assert result.id == 1
        assert result.titel == boek_data["titel"]
        assert result.auteur == boek_data["auteur"]
        assert result.isbn == boek_data["isbn"]
        assert result.jaar == boek_data["jaar"]
        mock_repo_instance.exists.assert_called_once_with(boek_data["isbn"])
        mock_repo_instance.create.assert_called_once_with(boek_data)

def test_create_boek_already_exists(boek_data):
    with patch("src.services.boekcreate.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists.return_value = True

        service = BoekService(repository=mock_repo_instance)
        with pytest.raises(BoekAlreadyExistsException):
            service.create_boek(boek_data)

        mock_repo_instance.exists.assert_called_once_with(boek_data["isbn"])
        mock_repo_instance.create.assert_not_called()

@pytest.mark.parametrize("invalid_data", [
    {"titel": "", "auteur": "Auteur1", "isbn": "9789000000001", "jaar": 2001},
    {"titel": "Titel", "auteur": "", "isbn": "9789000000002", "jaar": 2002},
    {"titel": "Titel", "auteur": "Auteur2", "isbn": "", "jaar": 2003},
    {"titel": "Titel", "auteur": "Auteur3", "isbn": "9789000000003", "jaar": None},
])
def test_create_boek_validation_exception(invalid_data):
    with patch("src.services.boekcreate.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists.return_value = False

        service = BoekService(repository=mock_repo_instance)
        with pytest.raises(BoekCreateValidationException):
            service.create_boek(invalid_data)

        mock_repo_instance.exists.assert_not_called()
        mock_repo_instance.create.assert_not_called()
