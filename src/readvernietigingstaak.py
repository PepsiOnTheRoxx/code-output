class VernietigingstaakNotFoundError(Exception):
    pass

class Vernietigingstaak:
    def __init__(self, id, naam, status):
        self.id = id
        self.naam = naam
        self.status = status

class VernietigingstaakRepository:
    def __init__(self):
        self._data = {}

    def add(self, vernietigingstaak):
        self._data[vernietigingstaak.id] = vernietigingstaak

    def get_by_id(self, id):
        try:
            return self._data[id]
        except KeyError:
            raise VernietigingstaakNotFoundError(f"Vernietigingstaak with id {id} not found.")

    def all(self):
        return list(self._data.values())

class DestructionTaskService:
    def __init__(self, repository=None):
        if repository is None:
            repository = VernietigingstaakRepository()
        self.repository = repository

    def read(self, id):
        return self.repository.get_by_id(id)

    def read_all(self):
        return self.repository.all()