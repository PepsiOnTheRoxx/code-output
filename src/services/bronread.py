from src.services.bronread_exceptions import BronNotFoundException, BronAccessException

class BronRepository:
    def get_by_id(self, bron_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

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