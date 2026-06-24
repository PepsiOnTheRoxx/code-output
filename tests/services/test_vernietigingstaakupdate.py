import pytest
from unittest.mock import patch, MagicMock
from src.services.vernietigingstaakupdate import VernietigingstaakService
from src.services.vernietigingstaakupdate_exceptions import VernietigingstaakNotFoundException, InvalidVernietigingstaakUpdateException

@pytest.fixture
def mock_repo():
    with patch("src.services.vernietigingstaakupdate.VernietigingstaakRepository") as repo_cls:
        repo = MagicMock()
        repo_cls.return_value = repo
        yield repo

@pytest.fixture
def service(mock_repo):
    return VernietigingstaakService(repository=mock_repo)

def test_update_vernietigingstaak_succesvol(service, mock_repo):
    taak_id = 42
    huidige_taak = MagicMock()
    mock_repo.get_by_id.return_value = huidige_taak
    update_data = {"status": "voltooid"}
    service.update(taak_id, update_data)
    mock_repo.get_by_id.assert_called_once_with(taak_id)
    for key, value in update_data.items():
        assert getattr(huidige_taak, key) == value
    mock_repo.save.assert_called_once_with(huidige_taak)

def test_update_vernietigingstaak_bestaat_niet(service, mock_repo):
    taak_id = 555
    mock_repo.get_by_id.return_value = None
    update_data = {"status": "geannuleerd"}
    with pytest.raises(VernietigingstaakNotFoundException):
        service.update(taak_id, update_data)
    mock_repo.get_by_id.assert_called_once_with(taak_id)
    mock_repo.save.assert_not_called()

def test_update_vernietigingstaak_onjuiste_gegevens(service, mock_repo):
    taak_id = 100
    huidige_taak = MagicMock()
    mock_repo.get_by_id.return_value = huidige_taak
    update_data = {"status": "ongeldige_status"}
    with patch("src.services.vernietigingstaakupdate.is_valid_status", return_value=False):
        with pytest.raises(InvalidVernietigingstaakUpdateException):
            service.update(taak_id, update_data)
    mock_repo.get_by_id.assert_called_once_with(taak_id)
    mock_repo.save.assert_not_called()

def test_update_vernietigingstaak_deelt_update(service, mock_repo):
    taak_id = 33
    huidige_taak = MagicMock()
    huidige_taak.status = "aangevraagd"
    huidige_taak.omschrijving = "Taakomschrijving oud"
    mock_repo.get_by_id.return_value = huidige_taak
    update_data = {"omschrijving": "Taakomschrijving nieuw"}
    service.update(taak_id, update_data)
    assert huidige_taak.status == "aangevraagd"
    assert huidige_taak.omschrijving == "Taakomschrijving nieuw"
    mock_repo.save.assert_called_once_with(huidige_taak)

def test_update_vernietigingstaak_save_exception(service, mock_repo):
    taak_id = 77
    huidige_taak = MagicMock()
    mock_repo.get_by_id.return_value = huidige_taak
    update_data = {"status": "in_behandeling"}
    mock_repo.save.side_effect = Exception("Database fout")
    with pytest.raises(Exception) as excinfo:
        service.update(taak_id, update_data)
    assert "Database fout" in str(excinfo.value)
    mock_repo.save.assert_called_once_with(huidige_taak)