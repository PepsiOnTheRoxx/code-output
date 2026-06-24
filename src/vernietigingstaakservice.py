class VernietigingstaakService:
    def __init__(self):
        # Simuleer storage
        self._taken = {
            1: {"id": 1, "status": "In afwachting", "datum": "2024-05-01"},
            2: {"id": 2, "status": "Voltooid", "datum": "2024-05-10"},
            3: {"id": 3, "status": "Geannuleerd", "datum": "2024-05-15"},
            4: {"id": 4, "status": "Bezig", "datum": "2024-06-01"},
        }

    def read_vernietigingstaak(self, taak_id):
        if taak_id not in self._taken:
            raise Exception(f"Vernietigingstaak met id {taak_id} bestaat niet")
        return self._taken[taak_id].copy()