from src.services.updatevernietigingstaak_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakUpdateException,
    VernietigingstaakUpdateNotAllowedException,
    VernietigingstaakServiceException,
)

class VernietigingstaakRepository:
    def get_by_id(self, taak_id):
        # Placeholder, om te worden gemockt in de tests
        pass
    def save(self, taak):
        # Placeholder, om te worden gemockt in de tests
        pass

class VernietigingstaakService:
    def __init__(self, repository=None):
        # Laat repository injecteren zodat deze te patchen is
        if repository is None:
            self.repository = VernietigingstaakRepository()
        else:
            self.repository = repository

    def update_vernietigingstaak(self, taak_id, update_data):
        try:
            taak = self.repository.get_by_id(taak_id)
            if taak is None:
                raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")
            if "naam" in update_data and update_data["naam"] == "":
                raise InvalidVernietigingstaakUpdateException("Naam mag niet leeg zijn.")
            for key, value in update_data.items():
                setattr(taak, key, value)
            self.repository.save(taak)
            return taak
        except Exception as e:
            # Gooi exceptie door als hij al verwachte types heeft
            if isinstance(e, (
                VernietigingstaakNotFoundException,
                InvalidVernietigingstaakUpdateException,
                VernietigingstaakUpdateNotAllowedException,
                VernietigingstaakServiceException,
            )):
                raise
            # Hergooi andere fouten als-gelijk met het originele bericht
            raise Exception(str(e))
