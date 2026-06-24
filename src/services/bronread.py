from src.services.bronread_exceptions import BronNotFoundException, BronAccessException

class BronRepository:
    def __init__(self):
        # In-memory "database"
        self._bronnen = [
            {'id': 1, 'naam': 'BronA'},
            {'id': 2, 'naam': 'BronB'},
        ]

    def get_by_id(self, bron_id):
        for bron in self._bronnen:
            if bron['id'] == bron_id:
                return bron
        return None

    def get_all(self):
        return list(self._bronnen)

class BronService:
    def __init__(self):
        self.repository = BronRepository()

    def get_bron_by_id(self, bron_id):
        try:
            bron = self.repository.get_by_id(bron_id)
        except BronAccessException:
            raise
        if bron is None:
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden")
        return bron

    def get_all_bronnen(self):
        return self.repository.get_all()
