import pytest
from src.updatevernietigingstaak import DestructionTaskService, VernietigingstaakNotFoundException, InvalidVernietigingstaakUpdateException

@pytest.fixture
def initial_taak():
    # assuming a Vernietigingstaak has id, naam, status
    return {'id': 1, 'naam': 'Taak1', 'status': 'open'}

@pytest.fixture
def service(initial_taak):
    # DestructionTaskService starts with one taak for tests
    s = DestructionTaskService()
    s._tasks = {initial_taak['id']: initial_taak.copy()}
    return s

def test_update_existing_taak_updates_attributes(service):
    update_data = {'id': 1, 'naam': 'Gewijzigd', 'status': 'gesloten'}
    updated = service.update(update_data)
    assert updated['id'] == 1
    assert updated['naam'] == 'Gewijzigd'
    assert updated['status'] == 'gesloten'

def test_update_non_existing_taak_raises(service):
    update_data = {'id': 999, 'naam': 'Niet bestaand', 'status': 'open'}
    with pytest.raises(VernietigingstaakNotFoundException):
        service.update(update_data)

def test_update_partial_fields_only_changes_given_fields(service):
    update_data = {'id': 1, 'status': 'in bewerking'}
    before = service._tasks[1].copy()
    updated = service.update(update_data)
    assert updated['id'] == 1
    assert updated['naam'] == before['naam']  # naam is onveranderd
    assert updated['status'] == 'in bewerking'

def test_update_with_invalid_id_type_raises(service):
    update_data = {'id': 'fout', 'naam': 'Onjuist'}
    with pytest.raises(InvalidVernietigingstaakUpdateException):
        service.update(update_data)

def test_update_rejects_unknown_fields(service):
    update_data = {'id': 1, 'onbekend': 'waarde'}
    with pytest.raises(InvalidVernietigingstaakUpdateException):
        service.update(update_data)

def test_update_keeps_other_fields_unchanged(service, initial_taak):
    update_data = {'id': 1, 'naam': 'Nieuwe naam'}
    service.update(update_data)
    taak = service._tasks[1]
    assert taak['naam'] == 'Nieuwe naam'
    assert taak['status'] == initial_taak['status']

def test_update_returns_updated_taak(service):
    update_data = {'id': 1, 'status': 'vernietigd'}
    result = service.update(update_data)
    assert result['status'] == 'vernietigd'
    assert result['id'] == 1
    assert 'naam' in result

def test_update_without_id_raises(service):
    update_data = {'naam': 'Geen id'}
    with pytest.raises(InvalidVernietigingstaakUpdateException):
        service.update(update_data)