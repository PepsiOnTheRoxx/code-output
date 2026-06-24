from src.services.vernietigingstaakread_exceptions import VernietigingstaakNotFoundException, UnauthorizedAccessException

class VernietigingstaakService:
    def __init__(self):
        # Simuleer dat er ergens storage/backing data is
        self._storage = {
            42: {
                "id": 42,
                "status": "aangemaakt",
                "omschrijving": "Test vernietiging",
                "object_type": 10
            },
            55: {
                "id": 55,
                "status": "voltooid",
                "omschrijving": "Opschonen database",
                "object_type": 10
            },
            123: {
                "id": 123,
                "status": "in_behandeling",
                "omschrijving": "Test andere status",
                "object_type": 10
            },
            7: {
                "id": 7,
                "status": "geweigerd",
                "omschrijving": "Geweigerd voorbeeld",
                "object_type": 10
            }
        }
        # Simuleer toegangscontrole
        self._unauthorized_ids = {7}

    def read(self, vernietigingstaak_id):
        if vernietigingstaak_id in self._unauthorized_ids:
            raise UnauthorizedAccessException()
        data = self._storage.get(vernietigingstaak_id)
        if not data:
            raise VernietigingstaakNotFoundException()
        return data