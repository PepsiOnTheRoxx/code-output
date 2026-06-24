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
        for key, value in new_data.items():
            if key == 'name':
                self.bron_data[bron_id]['name'] = value
            else:
                self.bron_data[bron_id]['attributes'][key] = value

    def get_bron(self, bron_id):
        if bron_id not in self.bron_data:
            raise BronNotFoundException(f'Bron with ID {bron_id} not found.')
        # return a deep copy to prevent test pollution
        return {
            'name': self.bron_data[bron_id]['name'],
            'attributes': dict(self.bron_data[bron_id]['attributes'])
        }

def test_update_bron_success():
    service = BronService()
    service.update_bron(12, {'name': 'Updated Bron', 15: 'Updated Value A'})
    updated_bron = service.get_bron(12)
    assert updated_bron['name'] == 'Updated Bron'
    assert updated_bron['attributes'][15] == 'Updated Value A'
    assert updated_bron['attributes'][16] == 'Value B'

def test_update_bron_partial_success():
    service = BronService()
    service.update_bron(12, {16: 'Updated Value B'})
    updated_bron = service.get_bron(12)
    assert updated_bron['name'] == 'Bron 1'
    assert updated_bron['attributes'][15] == 'Value A'
    assert updated_bron['attributes'][16] == 'Updated Value B'

def test_update_bron_not_found():
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.update_bron(99, {'name': 'Should Fail'})

def test_get_bron_not_found():
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.get_bron(99)