import re
from src.services.creategebruiker_exceptions import (
    GebruikerAlreadyExistsException,
    InvalidGebruikerDataException
)

class Gebruiker:
    def __init__(self, naam, emailadres):
        self.naam = naam
        self.emailadres = emailadres

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}

    def create_gebruiker(self, gebruiker_data):
        naam = gebruiker_data.get("naam", "")
        emailadres = gebruiker_data.get("emailadres")

        if not emailadres or not isinstance(emailadres, str) or not self._is_geldig_emailadres(emailadres):
            raise InvalidGebruikerDataException()

        if emailadres in self._gebruikers:
            raise GebruikerAlreadyExistsException()

        gebruiker = Gebruiker(naam, emailadres)
        self._gebruikers[emailadres] = gebruiker
        return gebruiker

    def _is_geldig_emailadres(self, emailadres):
        # Basic regex for validation of email address
        return re.match(r"[^@]+@[^@]+\.[^@]+", emailadres) is not None
