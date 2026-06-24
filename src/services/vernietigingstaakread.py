from src.services.vernietigingstaakread_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakReadException,
)

class VernietigingstaakService:
    def __init__(self):
        self._vernietigingstaken = [
            {'id': 1, 'status': 'in_progress'},
            {'id': 2, 'status': 'completed'}
        ]

    def get_vernietigingstaak_by_id(self, vernietigingstaak_id):
        try:
            for taak in self._vernietigingstaken:
                if taak['id'] == vernietigingstaak_id:
                    return taak
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak {vernietigingstaak_id} not found")
        except VernietigingstaakNotFoundException:
            raise
        except Exception as e:
            raise VernietigingstaakReadException(str(e))

    def get_all_vernietigingstaken(self):
        return list(self._vernietigingstaken)