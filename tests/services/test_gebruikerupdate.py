import pytest
from src.services.gebruikerupdate import GebruikerService
from src.services.gebruikerupdate_exceptions import GebruikerNietGevondenException, OngeldigeGebruikerDataException

@pytest.fixture
def gebruiker_service(monkeypatch):
    service = GebruikerService()
    service.vind_gebruiker_op_id = lambda gebruiker_id: None
    service.opslaan_gebruiker = lambda gebruiker_dict: None
    # Om eenvoudig monkeypatching te laten werken gebruiken we attributen,
    # maar voor assertions moeten we wrapper-mocks gebruiken
    class CallTracker:
        def __init__(self):
            self.called_with = []
            self.called = 0
        def __call__(self, *args, **kwargs):
            self.called += 1
            self.called_with.append((args, kwargs))
    service._vind_mock = CallTracker()
    service._opslaan_mock = CallTracker()
    def vind_op_id_patch(gebruiker_id):
        service._vind_mock(gebruiker_id)
        return service._vind_return
    def opslaan_patch(gebruiker_dict):
        service._opslaan_mock(gebruiker_dict)
    service.vind_gebruiker_op_id = vind_op_id_patch
    service.opslaan_gebruiker = opslaan_patch
    service._vind_return = None  # om per test te zetten
    return service

def test_update_gebruiker_succesvol(gebruiker_service):
    gebruiker_mock = {"id": 1, "naam": "Jan", "email": "jan@ex.com"}
    gebruiker_service._vind_return = gebruiker_mock
    payload = {"id": 1, "naam": "Jan Nieuw", "email": "jan_nieuw@ex.com"}
    gebruiker_service.update_gebruiker(payload)
    assert gebruiker_service._vind_mock.called == 1
    assert gebruiker_service._vind_mock.called_with[0][0][0] == 1
    assert gebruiker_service._opslaan_mock.called == 1
    args, kwargs = gebruiker_service._opslaan_mock.called_with[0]
    assert args[0]["naam"] == "Jan Nieuw"
    assert args[0]["email"] == "jan_nieuw@ex.com"

def test_update_gebruiker_bestaat_niet(gebruiker_service):
    gebruiker_service._vind_return = None
    payload = {"id": 99, "naam": "Onbekend", "email": "onbekend@ex.com"}
    with pytest.raises(GebruikerNietGevondenException):
        gebruiker_service.update_gebruiker(payload)
    assert gebruiker_service._vind_mock.called == 1
    assert gebruiker_service._vind_mock.called_with[0][0][0] == 99
    assert gebruiker_service._opslaan_mock.called == 0

def test_update_gebruiker_ongeldige_data(gebruiker_service):
    gebruiker_mock = {"id": 2, "naam": "Kees", "email": "kees@ex.com"}
    gebruiker_service._vind_return = gebruiker_mock
    payload = {"id": 2, "naam": "", "email": "geen_email"}
    with pytest.raises(OngeldigeGebruikerDataException):
        gebruiker_service.update_gebruiker(payload)
    assert gebruiker_service._opslaan_mock.called == 0

def test_update_gebruiker_id_verplicht(gebruiker_service):
    payload = {"naam": "Frans", "email": "frans@ex.com"}
    with pytest.raises(OngeldigeGebruikerDataException):
        gebruiker_service.update_gebruiker(payload)
    assert gebruiker_service._vind_mock.called == 0
    assert gebruiker_service._opslaan_mock.called == 0

def test_email_niet_aangepast_bij_leeg_emailveld(gebruiker_service):
    gebruiker_mock = {"id": 4, "naam": "Els", "email": "els@ex.com"}
    gebruiker_service._vind_return = gebruiker_mock
    payload = {"id": 4, "naam": "Els Update"}
    gebruiker_service.update_gebruiker(payload)
    assert gebruiker_service._opslaan_mock.called == 1
    updated_gebruiker = gebruiker_service._opslaan_mock.called_with[0][0][0]
    assert updated_gebruiker["email"] == "els@ex.com"
    assert updated_gebruiker["naam"] == "Els Update"
