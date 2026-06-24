from src.services.bronupdate_exceptions import BronUpdateNotFoundException, BronUpdateValidationException

class Bron:
    def __init__(self, bron_id, naam='', type=''):
        self.bron_id = bron_id
        self.naam = naam
        self.type = type

class BronService:
    _bron_db = {}

    def get_bron_by_id(self, bron_id):
        # Simuleer een database lookup
        return self._bron_db.get(bron_id)

    def validate_data(self, data):
        # Simpele validatie: naam mag niet leeg zijn indien aanwezig; type mag niet leeg zijn indien aanwezig
        if 'naam' in data and not data['naam']:
            raise BronUpdateValidationException('Naam mag niet leeg zijn')
        if 'type' in data and not data['type']:
            raise BronUpdateValidationException('Type mag niet leeg zijn')
        return True

    def save_bron(self, bron):
        # Simuleer database save
        self._bron_db[bron.bron_id] = bron

    def update_bron(self, bron_id, nieuwe_data):
        bron = self.get_bron_by_id(bron_id)
        if not bron:
            raise BronUpdateNotFoundException(f"Bron met id {bron_id} niet gevonden")
        self.validate_data(nieuwe_data)
        for key, value in nieuwe_data.items():
            setattr(bron, key, value)
        self.save_bron(bron)