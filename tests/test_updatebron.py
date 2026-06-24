import pytest

class BronNotFoundException(Exception):
    pass

class BronService:
    def __init__(self):
        self.bron_data = {
            12: {'name': 'Bron 1', 'attributes': {15: 'Value A', 16: 'Value B'}},
        }

    def update_bron(self, bron_id, new_data):
        if bron_id not in self.bron_data:
            raise BronNotFoundException(f'Bron with ID {bron_id} not found.')
        self.bron_data[bron_id].update(new_data)

    def get_bron(self, bron_id):
        if bron_id not in self.bron_data:
            raise BronNotFoundException(f'Bron with ID {bron_id} not found.')
        return self.bron_data[bron_id]

def test_update_bron_success():
    service = BronService()
    service.update_bron(12, {'name': 'Updated Bron', 15: 'Updated Value A'})
    updated_bron = service.get_bron(12)
    assert updated_bron['name'] == 'Updated Bron'
    assert updated_bron[15] == 'Updated Value A'
    assert updated_bron[16] == 'Value B'

def test_update_bron_partial_success():
    service = BronService()
    service.update_bron(12, {16: 'Updated Value B'})
    updated_bron = service.get_bron(12)
    assert updated_bron[16] == 'Updated Value B'
    assert updated_bron[15] == 'Value A'

def test_update_bron_not_found():
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.update_bron(99, {'name': 'Should Fail'})

def test_get_bron_not_found():
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.get_bron(99)