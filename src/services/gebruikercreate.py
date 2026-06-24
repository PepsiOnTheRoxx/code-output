from src.services.gebruikercreate_exceptions import (
    EmailAdresBestaatAlException,
    OngeldigEmailAdresException,
    OngeldigeNaamException
)
import re

class Gebruiker:
    def __init__(self, naam, email):
        self.naam = naam
        self.email = email

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}  # email: Gebruiker

    def maak_gebruiker(self, naam, email):
        if not isinstance(naam, str) or not naam.strip():
            raise OngeldigeNaamException("Naam is ongeldig of leeg.")
        if not isinstance(email, str) or not self._is_geldig_email(email):
            raise OngeldigEmailAdresException("Emailadres is ongeldig.")
        if email in self._gebruikers:
            raise EmailAdresBestaatAlException("Emailadres bestaat al.")
        gebruiker = Gebruiker(naam, email)
        self._gebruikers[email] = gebruiker
        return gebruiker

    def _is_geldig_email(self, email):
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(pattern, email) is not None