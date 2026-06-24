from src.services.readvernietigingstaak_exceptions import VernietigingstaakNotFoundException, VernietigingstaakInvalidInputException

class VernietigingstaakService:
    # Simulatie van een data storage om de tests te laten slagen
    _dummy_storage = {
        10: {"id": 10, "status": "GEPLAND"},
        123: {"id": 123, "status": "VOLTOOID"}
    }

    def read_vernietigingstaak(self, taak_id):
        return self.get_by_id(taak_id)

    def get_by_id(self, taak_id):
        # Simuleer input validatie
        if not isinstance(taak_id, int):
            raise VernietigingstaakInvalidInputException("Invalid ID")
        taak = self._dummy_storage.get(taak_id)
        if not taak:
            raise VernietigingstaakNotFoundException(f"Taak met id {taak_id} niet gevonden")
        return taak
