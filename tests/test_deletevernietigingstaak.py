import pytest
from src.deletevernietigingstaak import VernietigingstaakService
from src.deletevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException,
    UnauthorizedVernietigingstaakDeleteException
)

def test_delete_vernietigingstaak_happy_path(mocker):
    service = VernietigingstaakService()
    mock_delete = mocker.patch.object(service, "delete_by_id", return_value=True)
    result = service.delete_by_id(10, user_id=1)
    assert result is True
    mock_delete.assert_called_once_with(10, user_id=1)

def test_delete_vernietigingstaak_not_found(mocker):
    service = VernietigingstaakService()
    mocker.patch.object(service, "delete_by_id", side_effect=VernietigingstaakNotFoundException)
    with pytest.raises(VernietigingstaakNotFoundException):
        service.delete_by_id(999, user_id=1)

def test_delete_vernietigingstaak_error(mocker):
    service = VernietigingstaakService()
    mocker.patch.object(service, "delete_by_id", side_effect=VernietigingstaakDeleteException)
    with pytest.raises(VernietigingstaakDeleteException):
        service.delete_by_id(11, user_id=1)

def test_delete_vernietigingstaak_unauthorized(mocker):
    service = VernietigingstaakService()
    mocker.patch.object(service, "delete_by_id", side_effect=UnauthorizedVernietigingstaakDeleteException)
    with pytest.raises(UnauthorizedVernietigingstaakDeleteException):
        service.delete_by_id(10, user_id=99)

def test_delete_vernietigingstaak_invalid_id(mocker):
    service = VernietigingstaakService()
    mocker.patch.object(service, "delete_by_id", side_effect=ValueError("Invalid ID"))
    with pytest.raises(ValueError) as excinfo:
        service.delete_by_id(-1, user_id=1)
    assert "Invalid ID" in str(excinfo.value)