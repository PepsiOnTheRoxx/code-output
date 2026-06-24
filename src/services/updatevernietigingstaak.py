from src.services.updatevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakDataException,
    VernietigingstaakUpdateNotAllowedException,
    VernietigingstaakServiceException,
)

class VernietigingstaakRepository:
    def get_by_id(self, taak_id):
        # Plaatsvervanger, implementatie elders
        pass
    def save(self, taak):
        # Plaatsvervanger, implementatie elders
        pass

class VernietigingstaakService:
    def __init__(self):
        self.repository = VernietigingstaakRepository()

    def update_vernietigingstaak(self, taak_id, update_data):
        taak = self.repository.get_by_id(taak_id)
        if taak is None:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")
        if "naam" in update_data and not update_data["naam"]:
            from src.services.updatevernietigingstaak_exceptions import InvalidVernietigingstaakUpdateException
            raise InvalidVernietigingstaakUpdateException("Naam mag niet leeg zijn.")
        for key, value in update_data.items():
            setattr(taak, key, value)
        self.repository.save(taak)
        return taak