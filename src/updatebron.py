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
        return {
            'name': self.bron_data[bron_id]['name'],
            'attributes': dict(self.bron_data[bron_id]['attributes'])
        }