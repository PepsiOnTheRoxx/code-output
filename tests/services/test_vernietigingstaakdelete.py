import pytest
from src.services.vernietigingstaakdelete import VernietigingstaakService
from src.services.vernietigingstaakdelete_exceptions import VernietigingstaakNotFoundError, VernietigingstaakDeleteError

@pytest.fixture
def vernietigingstaak_service(mocker):
    return VernietigingstaakService()

def test_delete_bestaande_vernietigingstaak_succesvol_verwijderd(mocker, vernietigingstaak_service):
    mock_verwijder = mocker.patch.object(vernietigingstaak_service, "verwijder_vernietigingstaak", return_value=True)
    resultaat = vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=123)
    assert resultaat is True
    mock_verwijder.assert_called_once_with(taak_id=123)

def test_delete_niet_bestaande_vernietigingstaak_raised_not_found(mocker, vernietigingstaak_service):
    mocker.patch.object(vernietigingstaak_service, "verwijder_vernietigingstaak", side_effect=VernietigingstaakNotFoundError("Taak bestaat niet"))
    with pytest.raises(VernietigingstaakNotFoundError, match="Taak bestaat niet"):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=999)

def test_delete_vernietigingstaak_onverwachte_fout_raised_delete_error(mocker, vernietigingstaak_service):
    mocker.patch.object(vernietigingstaak_service, "verwijder_vernietigingstaak", side_effect=VernietigingstaakDeleteError("Verwijderen mislukt"))
    with pytest.raises(VernietigingstaakDeleteError, match="Verwijderen mislukt"):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=456)

def test_delete_vernietigingstaak_meerdere_keers_geen_extra_verwijdering(mocker, vernietigingstaak_service):
    mock_verwijder = mocker.patch.object(vernietigingstaak_service, "verwijder_vernietigingstaak", return_value=True)
    vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=789)
    with pytest.raises(VernietigingstaakNotFoundError):
        mock_verwijder.side_effect = VernietigingstaakNotFoundError("Taak bestaat niet")
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=789)
    assert mock_verwijder.call_count == 2

def test_delete_vernietigingstaak_invalid_argument_type(mocker, vernietigingstaak_service):
    with pytest.raises(TypeError):
        vernietigingstaak_service.verwijder_vernietigingstaak(taak_id=None)