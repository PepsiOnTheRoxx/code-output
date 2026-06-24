import pytest
from src.deletevernietigingstaak import VernietigingstaakService
from src.deletevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException,
    UnauthorizedVernietigingstaakDeleteException
)

def test_delete_vernietigingstaak_happy_path():
    service = VernietigingstaakService()
    result = service.delete_by_id(10, user_id=1)
    assert result is True

def test_delete_vernietigingstaak_not_found():
    service = VernietigingstaakService()
    with pytest.raises(VernietigingstaakNotFoundException):
        service.delete_by_id(999, user_id=1)

def test_delete_vernietigingstaak_error():
    service = VernietigingstaakService()
    with pytest.raises(VernietigingstaakDeleteException):
        service.delete_by_id(11, user_id=1)

def test_delete_vernietigingstaak_unauthorized():
    service = VernietigingstaakService()
    with pytest.raises(UnauthorizedVernietigingstaakDeleteException):
        service.delete_by_id(10, user_id=99)

def test_delete_vernietigingstaak_invalid_id():
    service = VernietigingstaakService()
    with pytest.raises(ValueError) as excinfo:
        service.delete_by_id(-1, user_id=1)
    assert "Invalid ID" in str(excinfo.value)
