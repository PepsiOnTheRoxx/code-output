import pytest
from unittest.mock import patch, MagicMock
from src.services.updatevernietigingstaak import VernietigingstaakService
from src.services.updatevernietigingstaak_exceptions import VernietigingstaakNotFoundException, InvalidVernietigingstaakUpdateException

@pytest.fixture
def service():
    return VernietigingstaakService()

def test_update_vernietigingstaak_success(service):
    taak_id = 42
    update_data = {"naam": "Nieuwe naam", "status": "wijziging"}
    mock_task = MagicMock()
    with patch("src.services.updatevernietigingstaak.VernietigingstaakRepository") as mock_repo:
        instance = mock_repo.return_value
        instance.get_by_id.return_value = mock_task
        instance.save.return_value = None
        s = VernietigingstaakService(repository=instance)
        result = s.update_vernietigingstaak(taak_id, update_data)
        instance.get_by_id.assert_called_once_with(taak_id)
        for k, v in update_data.items():
            assert getattr(mock_task, k) == v
        instance.save.assert_called_once_with(mock_task)
        assert result == mock_task

def test_update_vernietigingstaak_not_found(service):
    taak_id = 99
    update_data = {"naam": "Onbekend"}
    with patch("src.services.updatevernietigingstaak.VernietigingstaakRepository") as mock_repo:
        instance = mock_repo.return_value
        instance.get_by_id.return_value = None
        s = VernietigingstaakService(repository=instance)
        with pytest.raises(VernietigingstaakNotFoundException):
            s.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_invalid_update(service):
    taak_id = 13
    update_data = {"naam": ""}  # lege naam moet fout geven
    mock_task = MagicMock()
    with patch("src.services.updatevernietigingstaak.VernietigingstaakRepository") as mock_repo:
        instance = mock_repo.return_value
        instance.get_by_id.return_value = mock_task
        s = VernietigingstaakService(repository=instance)
        with pytest.raises(InvalidVernietigingstaakUpdateException):
            s.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_partial_update(service):
    taak_id = 17
    update_data = {"status": "in_behandeling"}
    mock_task = MagicMock()
    with patch("src.services.updatevernietigingstaak.VernietigingstaakRepository") as mock_repo:
        instance = mock_repo.return_value
        instance.get_by_id.return_value = mock_task
        instance.save.return_value = None
        s = VernietigingstaakService(repository=instance)
        s.update_vernietigingstaak(taak_id, update_data)
        assert mock_task.status == "in_behandeling"
        instance.save.assert_called_once_with(mock_task)

def test_update_vernietigingstaak_repository_save_failure(service):
    taak_id = 55
    update_data = {"naam": "Mislukt"}
    mock_task = MagicMock()
    with patch("src.services.updatevernietigingstaak.VernietigingstaakRepository") as mock_repo:
        instance = mock_repo.return_value
        instance.get_by_id.return_value = mock_task
        instance.save.side_effect = Exception("Databasefout")
        s = VernietigingstaakService(repository=instance)
        with pytest.raises(Exception) as excinfo:
            s.update_vernietigingstaak(taak_id, update_data)
        assert "Databasefout" in str(excinfo.value)
