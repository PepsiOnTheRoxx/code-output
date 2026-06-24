import pytest
from src.updatevernietigingstaak import VernietigingstaakService
from src.updatevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakDataException,
    UpdateNotAllowedException
)

def test_update_vernietigingstaak_success(mocker):
    taak_id = 123
    update_data = {
        'naam': 'Nieuwe Taak',
        'datum': '2024-07-01',
        'status': 'Gepland'
    }
    mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', return_value={'id': taak_id, 'naam': 'Oude Taak', 'datum': '2024-06-01', 'status': 'Aangevraagd'})
    mock_update = mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.update')
    service = VernietigingstaakService()
    result = service.update_vernietigingstaak(taak_id, update_data)
    mock_update.assert_called_once_with(taak_id, update_data)
    assert result['naam'] == 'Nieuwe Taak'
    assert result['datum'] == '2024-07-01'
    assert result['status'] == 'Gepland'

def test_update_vernietigingstaak_not_found(mocker):
    taak_id = 999
    update_data = {'naam': 'Test'}
    mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', return_value=None)
    service = VernietigingstaakService()
    with pytest.raises(VernietigingstaakNotFoundException):
        service.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_invalid_data(mocker):
    taak_id = 123
    invalid_update_data = {'naam': '', 'datum': 'foute-datum', 'status': 'Onbekend'}
    mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', return_value={'id': taak_id, 'naam': 'Taak', 'datum': '2024-06-01', 'status': 'Aangevraagd'})
    service = VernietigingstaakService()
    with pytest.raises(InvalidVernietigingstaakDataException):
        service.update_vernietigingstaak(taak_id, invalid_update_data)

def test_update_vernietigingstaak_update_not_allowed(mocker):
    taak_id = 123
    update_data = {'naam': 'Update Proberen'}
    bestaande_taak = {'id': taak_id, 'naam': 'Taak', 'datum': '2024-06-01', 'status': 'Voltooid'}
    mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', return_value=bestaande_taak)
    service = VernietigingstaakService()
    with pytest.raises(UpdateNotAllowedException):
        service.update_vernietigingstaak(taak_id, update_data)

def test_update_vernietigingstaak_partial_update(mocker):
    taak_id = 234
    update_data = {'naam': 'Gedeeltelijk Gewijzigde Taak'}
    bestaande_taak = {'id': taak_id, 'naam': 'Oude Taak', 'datum': '2024-07-01', 'status': 'Gepland'}
    mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.get_by_id', return_value=bestaande_taak)
    mock_update = mocker.patch('src.updatevernietigingstaak.VernietigingstaakRepository.update')
    service = VernietigingstaakService()
    result = service.update_vernietigingstaak(taak_id, update_data)
    assert result['naam'] == 'Gedeeltelijk Gewijzigde Taak'
    assert result['datum'] == '2024-07-01'
    assert result['status'] == 'Gepland'
    mock_update.assert_called_once_with(taak_id, {'naam': 'Gedeeltelijk Gewijzigde Taak'})