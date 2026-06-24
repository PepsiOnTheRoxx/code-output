from src.services.brondelete_exceptions import BronNotFoundException, BronDeleteException

class BronService:
    def bron_exists(self, bron_id):
        # Placeholder: implement data lookup
        raise NotImplementedError

    def delete_bron(self, bron_id):
        # Placeholder: implement delete logic
        raise NotImplementedError

    def delete(self, bron_id):
        if not self.bron_exists(bron_id):
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden")
        self.delete_bron(bron_id)
