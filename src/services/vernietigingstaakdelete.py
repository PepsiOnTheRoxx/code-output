from src.services.vernietigingstaakdelete_exceptions import VernietigingstaakNotFoundException, VernietigingstaakDeleteException

class VernietigingstaakService:
    def __init__(self):
        self._vernietigingstaken = {}  # Simuleer opslag

    def verwijder_vernietigingstaak(self, taak_id):
        if taak_id is None:
            raise TypeError("taak_id mag niet None zijn")
        if not isinstance(taak_id, int):
            raise TypeError("taak_id moet een integer zijn")
        if taak_id not in self._vernietigingstaken:
            raise VernietigingstaakNotFoundException("Taak bestaat niet")
        try:
            self._del_vernietigingstaak(taak_id)
        except Exception as exc:
            raise VernietigingstaakDeleteException("Verwijderen mislukt") from exc
        return True

    def _del_vernietigingstaak(self, taak_id):
        del self._vernietigingstaken[taak_id]
