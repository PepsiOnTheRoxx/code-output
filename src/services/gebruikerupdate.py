from src.services.gebruikerupdate_exceptions import (
    GebruikerNietGevondenException,
    OngeldigeGebruikerUpdateException,
    DatabaseFoutException,
)
import re

class GebruikerRepository:
    def get_by_id(self, gebruiker_id):
        raise NotImplementedError

    def update(self, gebruiker):
        raise NotImplementedError

class GebruikerService:
    def __init__(self):
        self.repo = GebruikerRepository()

    def update_gebruiker(self, gebruiker_id, data):
        gebruiker = self.repo.get_by_id(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNietGevondenException("Gebruiker niet gevonden")

        if not self._is_geldige_update_data(data):
            raise OngeldigeGebruikerUpdateException("Ongeldige gebruiker update data")

        for veld, waarde in data.items():
            if hasattr(gebruiker, veld):
                setattr(gebruiker, veld, waarde)
        try:
            self.repo.update(gebruiker)
        except DatabaseFoutException:
            raise
        return True

    def _is_geldige_update_data(self, data):
        if 'email' in data:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                return False
        return True