import pytest
from src.services.gebruikerupdate import GebruikerService
from src.services.gebruikerupdate_exceptions import GebruikerNietGevondenException, OngeldigeGebruikerDataException

@pytest.fixture
def gebruiker_service(mocker):
    service = GebruikerService()
    mocker.patch.object(service, "vind_gebruiker_op_id")
    mocker.patch.object(service, "opslaan_gebruiker")
    return service

def test_update_gebruiker_succesvol(gebruiker_service):
    gebruiker_mock = {"id": 1, "naam": "Jan", "email": "jan@ex.com"}
    gebruiker_service.vind_gebruiker_op_id.return_value = gebruiker_mock
    payload = {"id": 1, "naam": "Jan Nieuw", "email": "jan_nieuw@ex.com"}
    
    gebruiker_service.update_gebruiker(payload)

    gebruiker_service.vind_gebruiker_op_id.assert_called_once_with(1)
    gebruiker_service.opslaan_gebruiker.assert_called_once()
    args, kwargs = gebruiker_service.opslaan_gebruiker.call_args
    assert args[0]["naam"] == "Jan Nieuw"
    assert args[0]["email"] == "jan_nieuw@ex.com"

def test_update_gebruiker_bestaat_niet(gebruiker_service):
    gebruiker_service.vind_gebruiker_op_id.return_value = None
    payload = {"id": 99, "naam": "Onbekend", "email": "onbekend@ex.com"}
    
    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.update_gebruiker(payload)
    gebruiker_service.vind_gebruiker_op_id.assert_called_once_with(99)
    gebruiker_service.opslaan_gebruiker.assert_not_called()

def test_update_gebruiker_ongeldige_data(gebruiker_service):
    gebruiker_mock = {"id": 2, "naam": "Kees", "email": "kees@ex.com"}
    gebruiker_service.vind_gebruiker_op_id.return_value = gebruiker_mock
    payload = {"id": 2, "naam": "", "email": "geen_email"}
    
    with pytest.raises(OngeldigeGebruikerDataException):
        gebruiker_service.update_gebruiker(payload)
    gebruiker_service.opslaan_gebruiker.assert_not_called()

def test_update_gebruiker_id_verplicht(gebruiker_service):
    payload = {"naam": "Frans", "email": "frans@ex.com"}
    with pytest.raises(OngeldigeGebruikerDataException):
        gebruiker_service.update_gebruiker(payload)
    gebruiker_service.vind_gebruiker_op_id.assert_not_called()
    gebruiker_service.opslaan_gebruiker.assert_not_called()

def test_email_niet_aangepast_bij_leeg_emailveld(gebruiker_service):
    gebruiker_mock = {"id": 4, "naam": "Els", "email": "els@ex.com"}
    gebruiker_service.vind_gebruiker_op_id.return_value = gebruiker_mock
    payload = {"id": 4, "naam": "Els Update"}
    
    gebruiker_service.update_gebruiker(payload)
    
    gebruiker_service.opslaan_gebruiker.assert_called_once()
    updated_gebruiker = gebruiker_service.opslaan_gebruiker.call_args[0][0]
    assert updated_gebruiker["email"] == "els@ex.com"
    assert updated_gebruiker["naam"] == "Els Update"