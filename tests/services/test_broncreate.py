import pytest
from unittest.mock import patch, MagicMock
from src.services.broncreate import BronService
from src.services.broncreate_exceptions import BronCreateException, BronCreateValidationException

def test_create_bron_success():
    test_bron_data = {"naam": "TestBron", "attribute_15": "waarde1", "attribute_16": "waarde2"}
    bron_mock = MagicMock()
    with patch("src.services.broncreate.BronRepository") as repo_mock_cls:
        repo_mock = MagicMock()
        repo_mock.save_bron.return_value = bron_mock
        repo_mock.exists_bron.return_value = False
        repo_mock_cls.return_value = repo_mock
        service = BronService()
        result = service.create_bron(test_bron_data)
        repo_mock.save_bron.assert_called_once_with(test_bron_data)
        assert result == bron_mock

def test_create_bron_already_exists():
    test_bron_data = {"naam": "BestaandeBron", "attribute_15": "waarde1", "attribute_16": "waarde2"}
    with patch("src.services.broncreate.BronRepository") as repo_mock_cls:
        repo_mock = MagicMock()
        repo_mock.exists_bron.return_value = True
        repo_mock_cls.return_value = repo_mock
        service = BronService()
        with pytest.raises(BronCreateException):
            service.create_bron(test_bron_data)
        repo_mock.exists_bron.assert_called_once_with(test_bron_data["naam"])

def test_create_bron_invalid_data():
    invalid_bron_data = {"naam": "", "attribute_15": None, "attribute_16": ""}
    with patch("src.services.broncreate.BronRepository") as repo_mock_cls:
        repo_mock = MagicMock()
        repo_mock.exists_bron.return_value = False
        repo_mock_cls.return_value = repo_mock
        service = BronService()
        with pytest.raises(BronCreateValidationException):
            service.create_bron(invalid_bron_data)

def test_create_bron_repository_error():
    bron_data = {"naam": "NieuweBron", "attribute_15": "waarde1", "attribute_16": "waarde2"}
    with patch("src.services.broncreate.BronRepository") as repo_mock_cls:
        repo_mock = MagicMock()
        repo_mock.exists_bron.return_value = False
        repo_mock.save_bron.side_effect = Exception("Database fout")
        repo_mock_cls.return_value = repo_mock
        service = BronService()
        with pytest.raises(Exception) as excinfo:
            service.create_bron(bron_data)
        assert "Database fout" in str(excinfo.value)
