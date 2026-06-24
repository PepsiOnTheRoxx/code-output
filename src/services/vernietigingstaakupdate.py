from src.services.vernietigingstaakupdate_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakUpdateException,
)
from src.services.vernietigingstaakupdate import is_valid_status


class VernietigingstaakRepository:
    def get_by_id(self, taak_id):
        raise NotImplementedError

    def save(self, task):
        raise NotImplementedError


class VernietigingstaakService:
    def __init__(self, repository=None):
        self.repository = repository or VernietigingstaakRepository()

    def update(self, taak_id, update_data):
        taak = self.repository.get_by_id(taak_id)
        if taak is None:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak {taak_id} niet gevonden")
        for key, value in update_data.items():
            if key == "status":
                if not is_valid_status(value):
                    raise InvalidVernietigingstaakUpdateException(f"Ongeldige status: {value}")
            setattr(taak, key, value)
        self.repository.save(taak)