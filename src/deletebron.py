class BronNotFoundException(Exception):
    pass

class Bron:
    def __init__(self, bron_id, naam):
        self.bron_id = bron_id
        self.naam = naam

class BronRepository:
    def __init__(self):
        self._bronnen = {}

    def add(self, bron):
        self._bronnen[bron.bron_id] = bron

    def get(self, bron_id):
        return self._bronnen.get(bron_id)

    def delete(self, bron_id):
        if bron_id in self._bronnen:
            del self._bronnen[bron_id]
            return True
        return False

class BronService:
    def __init__(self):
        self.bron_repository = BronRepository()
        self._bron_id_seq = 1

    def create_bron(self, name):
        bron = Bron(self._bron_id_seq, name)
        self.bron_repository.add(bron)
        self._bron_id_seq += 1
        return bron.bron_id

    def get_bron(self, bron_id):
        bron = self.bron_repository.get(bron_id)
        if bron is None:
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden.")
        return bron

    def delete_bron(self, bron_id):
        bron = self.bron_repository.get(bron_id)
        if bron is None:
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden.")
        self.bron_repository.delete(bron_id)
        return None