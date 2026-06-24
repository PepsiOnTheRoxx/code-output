import pytest
from src.updatebron import BronService
from src.updatebron_exceptions import BronNotFoundException, InvalidBronDataException, BronUpdateNotAllowedException

@pytest.fixture
def bron_service():
    return BronService()

@pytest.fixture
def existing_bron():
    # Simuleer een bestaande 'Bron'
    return {
        'id': 1,
        'naam': 'Oorspronkelijke Bron',
        'omschrijving': 'Oorspronkelijke omschrijving'
    }

def test_update_bron_succes(bron_service, existing_bron):
    bron_service._bronnen = {1: existing_bron.copy()}
    nieuwe_data = {'naam': 'Nieuwe Bron', 'omschrijving': 'Nieuwe omschrijving'}
    updated = bron_service.update_bron(1, nieuwe_data)
    assert updated['id'] == 1
    assert updated['naam'] == 'Nieuwe Bron'
    assert updated['omschrijving'] == 'Nieuwe omschrijving'

def test_update_bron_not_found(bron_service):
    bron_service._bronnen = {}
    nieuwe_data = {'naam': 'Nieuwe Bron', 'omschrijving': 'Nieuwe omschrijving'}
    with pytest.raises(BronNotFoundException):
        bron_service.update_bron(999, nieuwe_data)

def test_update_bron_invalid_data(bron_service, existing_bron):
    bron_service._bronnen = {1: existing_bron.copy()}
    nieuwe_data = {'naam': '', 'omschrijving': 'Nog een omschrijving'}
    with pytest.raises(InvalidBronDataException):
        bron_service.update_bron(1, nieuwe_data)

def test_update_bron_update_not_allowed(bron_service, existing_bron):
    bron_service._bronnen = {1: existing_bron.copy()}
    # Simuleer situatie waarin update niet is toegestaan, bijvoorbeeld locked bron
    bron_service._locked_bronnen = {1}
    nieuwe_data = {'naam': 'Nieuwe Bron', 'omschrijving': 'Nieuwe omschrijving'}
    with pytest.raises(BronUpdateNotAllowedException):
        bron_service.update_bron(1, nieuwe_data)

def test_update_bron_partial_update(bron_service, existing_bron):
    bron_service._bronnen = {1: existing_bron.copy()}
    nieuwe_data = {'omschrijving': 'Aangepaste omschrijving'}
    updated = bron_service.update_bron(1, nieuwe_data)
    assert updated['id'] == 1
    assert updated['naam'] == 'Oorspronkelijke Bron'
    assert updated['omschrijving'] == 'Aangepaste omschrijving'

def test_update_bron_no_changes(bron_service, existing_bron):
    bron_service._bronnen = {1: existing_bron.copy()}
    nieuwe_data = {}
    updated = bron_service.update_bron(1, nieuwe_data)
    assert updated == existing_bron
