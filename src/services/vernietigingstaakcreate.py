from src.services.vernietigingstaakcreate_exceptions import (
    VernietigingstaakAlreadyExistsException,
    InvalidVernietigingstaakDataException,
    DatabaseException,
)

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
        raise NotImplementedError

    def _save(self, taak_data):
        raise NotImplementedError
