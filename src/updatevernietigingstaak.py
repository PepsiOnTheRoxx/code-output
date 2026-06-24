class VernietigingstaakNotFoundException(Exception):
    pass

class InvalidVernietigingstaakDataException(Exception):
    pass

class Vernietigingstaak:
    def __init__(self, taak_id, naam, status):
        self.taak_id = taak_id
        self.naam = naam
        self.status = status

class VernietigingstaakRepository:
    def __init__(self):
        # Simuleer een storage in memory
        self._taken = {}

    def get_by_id(self, taak_id):
        if taak_id in self._taken:
            return self._taken[taak_id]
        else:
            return None

    def update(self, taak):
        self._taken[taak.taak_id] = taak
        return taak

    def add(self, taak):
        self._taken[taak.taak_id] = taak

# Service voor het updaten van een vernietigingstaak
class DestructionTaskService:
    def __init__(self, repository=None):
        if repository is None:
            repository = VernietigingstaakRepository()
        self.repository = repository

    def update_vernietigingstaak(self, taak_id, naam=None, status=None):
        taak = self.repository.get_by_id(taak_id)
        if taak is None:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")

        if naam is not None:
            if not isinstance(naam, str) or not naam.strip():
                raise InvalidVernietigingstaakDataException("Naam kan niet leeg zijn.")
            taak.naam = naam
        if status is not None:
            if status not in ['pending', 'in_progress', 'completed']:
                raise InvalidVernietigingstaakDataException("Ongeldige status.")
            taak.status = status

        updated_taak = self.repository.update(taak)
        return updated_taak

# Optioneel: instantie voor testdoeleinden
# repo = VernietigingstaakRepository()
# service = DestructionTaskService(repo)
# taak = Vernietigingstaak(taak_id=1, naam='TaakX', status='pending')
# repo.add(taak)
# service.update_vernietigingstaak(1, naam='Nieuwe naam', status='in_progress')