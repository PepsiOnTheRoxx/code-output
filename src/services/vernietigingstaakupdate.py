from src.services.vernietigingstaakupdate_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakUpdateException,
)

class VernietigingstaakService:
    def __init__(self, repository):
        self.repository = repository

    def update_vernietigingstaak(self, update_data):
        if not update_data or not isinstance(update_data, dict):
            raise InvalidVernietigingstaakUpdateException()
        taak_id = update_data.get("id")
        if not taak_id or str(taak_id).strip() == "":
            raise InvalidVernietigingstaakUpdateException()
        bestaande_taak = self.repository.get_by_id(taak_id)
        if bestaande_taak is None:
            raise VernietigingstaakNotFoundException()
        taak_to_update = bestaande_taak.copy()
        for key, value in update_data.items():
            if key == "id":
                continue
            if value is not None:
                taak_to_update[key] = value
        self.repository.update(taak_id, taak_to_update)
        return taak_to_update

class VernietigingstaakRepository:
    # Dummy class so tests can patch this and import works
    pass
