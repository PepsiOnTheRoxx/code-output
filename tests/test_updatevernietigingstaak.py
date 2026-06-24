import pytest
from src.updatevernietigingstaak import VernietigingstaakService
from src.updatevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakDataException,
    UpdateNotAllowedException
)

def test_update_vernietigingstaak_success(monkeypatch):
    taak_id = 123
    update_data = {
        'naam': 'Nieuwe Taak',
        'datum': '2024-07-01',
        'status': 'Gepland'
    }
    bestaande = {'id': taak_id, 'naam': 'Oude Taak', 'datum': '2024-06-01', 'status': 'Aangevraagd'}
    def fake_get_by_id(tid):
        assert tid == taak_id
        return dict(bestaande)
    called = {}
    def fake_update(tid, data):
        called['called'] = True
        assert tid == taak_id
        assert data == update_data
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', fake_get_by_id)
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.update', fake_update)
    service = VernietigingstaakService()
    result = service.update_vernietigingstaak(taak_id, update_data)
    assert result['naam'] == 'Nieuwe Taak'
    assert result['datum'] == '2024-07-01'
    assert result['status'] == 'Gepland'
    assert called['called'] is True

def test_update_vernietigingstaak_not_found(monkeypatch):
    taak_id = 999
    update_data = {'naam': 'Test'}
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', lambda tid: None)
    service = VernietigingstaakService()
    with pytest.raises(VernietigingstaakNotFoundException):
        service.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_invalid_data(monkeypatch):
    taak_id = 123
    invalid_update_data = {'naam': '', 'datum': 'foute-datum', 'status': 'Onbekend'}
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', lambda tid: {'id': taak_id, 'naam': 'Taak', 'datum': '2024-06-01', 'status': 'Aangevraagd'})
    service = VernietigingstaakService()
    with pytest.raises(InvalidVernietigingstaakDataException):
        service.update_vernietigingstaak(taak_id, invalid_update_data)

def test_update_vernietigingstaak_update_not_allowed(monkeypatch):
    taak_id = 123
    update_data = {'naam': 'Update Proberen'}
    bestaande_taak = {'id': taak_id, 'naam': 'Taak', 'datum': '2024-06-01', 'status': 'Voltooid'}
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', lambda tid: dict(bestaande_taak))
    service = VernietigingstaakService()
    with pytest.raises(UpdateNotAllowedException):
        service.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_partial_update(monkeypatch):
    taak_id = 234
    update_data = {'naam': 'Gedeeltelijk Gewijzigde Taak'}
    bestaande_taak = {'id': taak_id, 'naam': 'Oude Taak', 'datum': '2024-07-01', 'status': 'Gepland'}
    calls = {}
    def fake_get_by_id(tid):
        assert tid == taak_id
        return dict(bestaande_taak)
    def fake_update(tid, data):
        calls['called'] = True
        assert tid == taak_id
        assert data == update_data
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', fake_get_by_id)
    monkeypatch.setattr('src.updatevernietigingstaak.VernietigingstaakRepository.update', fake_update)
    service = VernietigingstaakService()
    result = service.update_vernietigingstaak(taak_id, update_data)
    assert result['naam'] == 'Gedeeltelijk Gewijzigde Taak'
    assert result['datum'] == '2024-07-01'
    assert result['status'] == 'Gepland'
    assert calls['called'] is True
