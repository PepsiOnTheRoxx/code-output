from src.services.vernietigingstaakdelete_exceptions import VernietigingstaakNotFoundError, VernietigingstaakDeleteError

class VernietigingstaakService:
    def __init__(self):
        self._vernietigingstaken = {}  # Simuleer opslag

    def verwijder_vernietigingstaak(self, taak_id):
        if not isinstance(taak_id, int):
            raise TypeError("taak_id moet een integer zijn")
        if taak_id is None:
            raise TypeError("taak_id mag niet None zijn")
        if taak_id not in self._vernietigingstaken:
            raise VernietigingstaakNotFoundError("Taak bestaat niet")
        try:
            del self._vernietigingstaken[taak_id]
        except Exception as exc:
            raise VernietigingstaakDeleteError("Verwijderen mislukt") from exc
        return True