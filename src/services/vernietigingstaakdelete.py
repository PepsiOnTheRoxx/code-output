from src.services.vernietigingstaakdelete_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException
)

# In-memory datastore voor demo/test/voorbeeld
class SimpleDatastore:
    def __init__(self):
        self.data = {}
    def add(self, taak_id, taak):
        self.data[taak_id] = taak
    def get(self, taak_id):
        if taak_id not in self.data:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")
        return self.data[taak_id]
    def delete(self, taak_id):
        if taak_id not in self.data:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")
        del self.data[taak_id]

class VernietigingstaakService:
    def __init__(self, datastore=None):
        self._datastore = datastore or SimpleDatastore()
    def get_by_id(self, taak_id):
        return self._datastore.get(taak_id)
    def delete_by_id(self, taak_id):
        try:
            self._datastore.delete(taak_id)
        except Exception as e:
            # In werkelijkheid kun je hier afhankelijk van 'e' een specifieke exceptie raisen
            raise VernietigingstaakDeleteException(str(e))
    def delete_vernietigingstaak(self, taak_id):
        try:
            self.get_by_id(taak_id)
        except VernietigingstaakNotFoundException:
            raise
        self.delete_by_id(taak_id)
