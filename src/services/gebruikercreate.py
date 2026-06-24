from src.services.gebruikercreate_exceptions import (
    GebruikerAlreadyExistsException,
    InvalidGebruikerDataException,
    StorageException,
)

class GebruikerService:
    def create(self, gebruiker_data):
        self._validate_gebruiker_data(gebruiker_data)
        if self._bestaat_gebruiker(gebruiker_data):
            raise GebruikerAlreadyExistsException()
        return self._opslaan_gebruiker(gebruiker_data)

    def _validate_gebruiker_data(self, gebruiker_data):
        if not isinstance(gebruiker_data, dict):
            raise InvalidGebruikerDataException()
        naam = gebruiker_data.get("naam", "")
        email = gebruiker_data.get("email", "")
        if not (isinstance(naam, str) and naam.strip()):
            raise InvalidGebruikerDataException()
        if not (isinstance(email, str) and "@" in email and "." in email):
            raise InvalidGebruikerDataException()

    def _bestaat_gebruiker(self, gebruiker_data):
        raise NotImplementedError

    def _opslaan_gebruiker(self, gebruiker_data):
        raise NotImplementedError
