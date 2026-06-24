from src.creategebruiker_exceptions import *

import re

class Gebruiker:
    def __init__(self, naam, email):
        self.naam = naam
        self.email = email

class GebruikerService:
    def __init__(self):
        self._gebruikers = []

    def create_gebruiker(self, naam, email):
        if not naam:
            raise ValueError("Naam mag niet leeg zijn")
        if not email:
            raise ValueError("Email mag niet leeg zijn")
        if not self._is_geldig_email(email):
            raise OngeldigEmailadresException("Ongeldig emailadres")
        for gebruiker in self._gebruikers:
            if gebruiker.naam == naam and gebruiker.email == email:
                raise GebruikerBestaatAlException("Gebruiker bestaat al")
        gebruiker = Gebruiker(naam=naam, email=email)
        self._gebruikers.append(gebruiker)
        return gebruiker

    def _is_geldig_email(self, email):
        regex = r"^[\w\.\+\-]+@[\w]+\.[\w]{2,}$"
        return re.match(regex, email) is not None
