import pytest
from unittest.mock import MagicMock, patch
from src.vernietigingstaakservice import VernietigingstaakService

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_delete_existing_taak_success(service):
    taak_id = 123
    service._get_taak_by_id = MagicMock(return_value={"id": taak_id})
    service._delete_taak = MagicMock(return_value=True)
    result = service.delete_vernietigingstaak(taak_id)
    service._delete_taak.assert_called_once_with(taak_id)
    assert result is True

def test_delete_non_existing_taak_raises_error(service):
    taak_id = 555
    service._get_taak_by_id = MagicMock(return_value=None)
    with pytest.raises(ValueError):
        service.delete_vernietigingstaak(taak_id)

def test_delete_taak_deletion_failure(service):
    taak_id = 456
    service._get_taak_by_id = MagicMock(return_value={"id": taak_id})
    service._delete_taak = MagicMock(return_value=False)
    result = service.delete_vernietigingstaak(taak_id)
    assert result is False

def test_delete_taak_calls_correct_methods(service):
    taak_id = 789
    service._get_taak_by_id = MagicMock(return_value={"id": taak_id})
    service._delete_taak = MagicMock(return_value=True)
    service.delete_vernietigingstaak(taak_id)
    service._get_taak_by_id.assert_called_once_with(taak_id)
    service._delete_taak.assert_called_once_with(taak_id)

def test_delete_taak_invalid_id(service):
    invalid_id = None
    with pytest.raises(TypeError):
        service.delete_vernietigingstaak(invalid_id)