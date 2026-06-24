from src.services.brondelete_exceptions import BronNotFoundException

class BronService:
    def __init__(self):
        # Gebruik een simpele in-memory "database" als dict
        self._bronnen = {}

    def get_bron_by_id(self, bron_id):
        return self._bronnen.get(bron_id, None)

    def delete_bron_by_id(self, bron_id):
        if bron_id in self._bronnen:
            del self._bronnen[bron_id]
        else:
            raise BronNotFoundException()

    def delete_bron(self, bron_id):
        bron = self.get_bron_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException()
        self.delete_bron_by_id(bron_id)
