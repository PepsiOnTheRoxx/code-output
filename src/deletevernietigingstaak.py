class VernietigingstaakNotFoundException(Exception):
    pass

class Vernietigingstaak:
    def __init__(self, taak_id):
        self.taak_id = taak_id

class VernietigingstaakRepository:
    def __init__(self):
        self._taken = {}

    def add(self, taak: Vernietigingstaak):
        self._taken[taak.taak_id] = taak

    def get(self, taak_id):
        return self._taken.get(taak_id)

    def delete(self, taak_id):
        if taak_id in self._taken:
            del self._taken[taak_id]
        else:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")

class DestructionTaskService:
    def __init__(self, repository=None):
        if repository is None:
            self.repository = VernietigingstaakRepository()
        else:
            self.repository = repository

    def delete_vernietigingstaak(self, taak_id):
        taak = self.repository.get(taak_id)
        if taak is None:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")
        self.repository.delete(taak_id)
        return True