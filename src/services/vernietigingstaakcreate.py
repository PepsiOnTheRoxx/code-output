from src.services.vernietigingstaakcreate_exceptions import (
    VernietigingstaakAlreadyExistsException,
    InvalidVernietigingstaakDataException,
    DatabaseException,
)

# Simpele in-memory store voor demo/test doeleinden
_vernietigingstaak_store = []

class VernietigingstaakService:
    REQUIRED_ATTRIBUTES = ["attribute_10", "attribute_11", "attribute_12"]

    def create_vernietigingstaak(self, taak_data):
        if not isinstance(taak_data, dict):
            raise InvalidVernietigingstaakDataException("Data is not a dictionary or is None")
        for attr in self.REQUIRED_ATTRIBUTES:
            if attr not in taak_data:
                raise InvalidVernietigingstaakDataException(f"Missing required attribute: {attr}")
        if self._exists(taak_data):
            raise VernietigingstaakAlreadyExistsException("Vernietigingstaak already exists")
        try:
            return self._save(taak_data)
        except DatabaseException as ex:
            raise ex

    def _exists(self, taak_data):
        # Eenvoudig: check of een bestaand taak exact deze combinaties van attributen heeft
        for bestaande in _vernietigingstaak_store:
            if all(
                bestaande.get(attr) == taak_data.get(attr)
                for attr in self.REQUIRED_ATTRIBUTES
            ):
                return True
        return False

    def _save(self, taak_data):
        try:
            # Simuleer DB probleem
            if taak_data.get("force_db_error"):
                raise DatabaseException("DB error")
            # Fake primary key (ID) uitschrijven op basis van aantal items + 1
            nieuwe_id = len(_vernietigingstaak_store) + 1
            taak_met_id = dict(taak_data)
            taak_met_id["id"] = nieuwe_id
            _vernietigingstaak_store.append(taak_met_id)
            return nieuwe_id
        except Exception as e:
            # Opnieuw DatabaseException als het geen programmeerfout is
            if isinstance(e, DatabaseException):
                raise
            raise DatabaseException("Could not save Vernietigingstaak")
