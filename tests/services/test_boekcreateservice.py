import pytest
from unittest.mock import MagicMock, patch
from src.services.boekcreateservice import BoekCreateService
from src.services.boekcreateservice_exceptions import BoekAlreadyExistsException, InvalidBoekDataException

@pytest.fixture
def fake_boek_data():
    return {
        "titel": "Test Boek",
        "auteur": "Auteur Naam",
        "isbn": "1234567890"
    }

@pytest.fixture
def boek_service():
    return BoekCreateService()

def test_create_boek_success(fake_boek_data):
    with patch("src.services.boekcreateservice.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists_by_isbn.return_value = False
        mock_repo_instance.add.return_value = MagicMock(id=1, **fake_boek_data)
        service = BoekCreateService()
        result = service.create_boek(fake_boek_data)
        assert result.titel == fake_boek_data["titel"]
        assert result.auteur == fake_boek_data["auteur"]
        assert result.isbn == fake_boek_data["isbn"]

def test_create_boek_already_exists(fake_boek_data):
    with patch("src.services.boekcreateservice.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists_by_isbn.return_value = True
        service = BoekCreateService()
        with pytest.raises(BoekAlreadyExistsException):
            service.create_boek(fake_boek_data)

@pytest.mark.parametrize("invalid_data", [
    {},  # completely empty
    {"titel": "Test"},  # missing some required fields
    {"auteur": "Auteur Naam"},  # missing isbn and title
    {"titel": "", "auteur": "", "isbn": ""},  # all fields empty
])
def test_create_boek_invalid_data(invalid_data):
    with patch("src.services.boekcreateservice.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists_by_isbn.return_value = False
        service = BoekCreateService()
        with pytest.raises(InvalidBoekDataException):
            service.create_boek(invalid_data)

def test_create_boek_persists_to_repository(fake_boek_data):
    with patch("src.services.boekcreateservice.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists_by_isbn.return_value = False
        mock_repo_instance.add.return_value = MagicMock(id=42, **fake_boek_data)
        service = BoekCreateService()
        result = service.create_boek(fake_boek_data)
        mock_repo_instance.add.assert_called_once()
        assert result.id == 42

def test_create_boek_repository_called_with_expected_data(fake_boek_data):
    with patch("src.services.boekcreateservice.BoekRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.exists_by_isbn.return_value = False
        mock_repo_instance.add.return_value = MagicMock(id=2, **fake_boek_data)
        service = BoekCreateService()
        service.create_boek(fake_boek_data)
        args, kwargs = mock_repo_instance.add.call_args
        assert kwargs["titel"] == fake_boek_data["titel"]
        assert kwargs["auteur"] == fake_boek_data["auteur"]
        assert kwargs["isbn"] == fake_boek_data["isbn"]