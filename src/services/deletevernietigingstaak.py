from src.services.deletevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException
)

# Simulated in-memory 'database' for Vernietigingstaak objects.
_in_memory_db = {}

class Vernietigingstaak:
    def __init__(self, identificatie):
        self.identificatie = identificatie

def seed_vernietigingstaken(ids):
    _in_memory_db.clear()
    for i in ids:
        _in_memory_db[i] = Vernietigingstaak(i)

class VernietigingstaakService:
    def get_vernietigingstaak_by_id(self, identificatie):
        return _in_memory_db.get(identificatie)

    def delete_vernietigingstaak_from_db(self, vernietigingstaak):
        identificatie = vernietigingstaak.identificatie
        if identificatie in _in_memory_db:
            try:
                del _in_memory_db[identificatie]
            except Exception as e:
                raise VernietigingstaakDeleteException(f'Error during delete: {e}')
        else:
            # If for some reason not found at deletion time, raise exception
            raise VernietigingstaakDeleteException(f'Vernietigingstaak {identificatie} already deleted or missing')

    def delete_vernietigingstaak(self, identificatie):
        vernietigingstaak = self.get_vernietigingstaak_by_id(identificatie)
        if vernietigingstaak is None:
            raise VernietigingstaakNotFoundException(f'Vernietigingstaak with id {identificatie} not found')
        try:
            self.delete_vernietigingstaak_from_db(vernietigingstaak)
        except VernietigingstaakDeleteException:
            raise
