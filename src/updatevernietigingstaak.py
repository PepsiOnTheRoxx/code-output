class VernietigingstaakNotFoundException(Exception):
    pass

class InvalidVernietigingstaakUpdateException(Exception):
    pass

class DestructionTaskService:
    def __init__(self):
        self._tasks = {}

    def update(self, data):
        if not isinstance(data, dict):
            raise InvalidVernietigingstaakUpdateException("Update data moet een dict zijn.")

        # Controleer of id aanwezig is en valide
        if "id" not in data:
            raise InvalidVernietigingstaakUpdateException("Veld 'id' ontbreekt in update data.")

        taak_id = data['id']
        if not isinstance(taak_id, int):
            raise InvalidVernietigingstaakUpdateException("Id moet een integer zijn.")

        if taak_id not in self._tasks:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")

        # Alleen deze velden mogen geüpdatet worden
        toegestane_velden = {"id", "naam", "status"}
        onbekende = set(data.keys()) - toegestane_velden
        if onbekende:
            raise InvalidVernietigingstaakUpdateException("Onbekende velden in update data.")

        # Haal bestaande taak
        taak = self._tasks[taak_id]

        # Pas alleen velden aan die zijn opgegeven (behalve "id")
        for veld in ("naam", "status"):
            if veld in data:
                taak[veld] = data[veld]

        # Return de gewijzigde taak (kopie)
        return dict(taak)