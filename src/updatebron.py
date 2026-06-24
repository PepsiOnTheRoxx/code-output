from src.updatebron_exceptions import *

class BronService:
    def __init__(self):
        self._bronnen = {}
        self._locked_bronnen = set()

    def update_bron(self, bron_id, nieuwe_data):
        if bron_id not in self._bronnen:
            raise BronNotFoundException()
        if hasattr(self, '_locked_bronnen') and bron_id in self._locked_bronnen:
            raise BronUpdateNotAllowedException()

        bron = self._bronnen[bron_id]
        updated_bron = bron.copy()

        allowed_keys = {'naam', 'omschrijving'}

        for key in nieuwe_data:
            if key not in allowed_keys:
                continue
            if key == 'naam' and nieuwe_data[key] == '':
                raise InvalidBronDataException()
        
        if 'naam' in nieuwe_data:
            updated_bron['naam'] = nieuwe_data['naam']
        if 'omschrijving' in nieuwe_data:
            updated_bron['omschrijving'] = nieuwe_data['omschrijving']

        self._bronnen[bron_id] = updated_bron
        return updated_bron
