class VernietigingstaakNotFound(Exception):
    pass

class Vernietigingstaak:
    def __init__(self, id, description):
        self.id = id
        self.description = description

class DestructionTaskService:
    def __init__(self):
        self._tasks = {}

    def read(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        try:
            return self._tasks[id]
        except KeyError:
            raise VernietigingstaakNotFound(f"Vernietigingstaak with id {id} not found.")

    def read_all(self):
        return list(self._tasks.values())