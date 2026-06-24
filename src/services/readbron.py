from src.services.readbron_exceptions import BronNotFoundException, BronReadException

class BronRepository:
    def get_bron_by_id(self, bron_id):
        # Placeholder for the actual database/repository logic
        raise NotImplementedError

class BronService:
    def __init__(self):
        self.repository = BronRepository()

    def read_bron(self, bron_id):
        if not isinstance(bron_id, int):
            raise TypeError("Bron ID must be an integer.")
        try:
            bron = self.repository.get_bron_by_id(bron_id)
            if bron is None:
                raise BronNotFoundException(f"Bron with id {bron_id} not found.")
            return bron
        except BronNotFoundException:
            raise
        except Exception as e:
            raise BronReadException(f"Failed to read Bron with id {bron_id}: {e}")