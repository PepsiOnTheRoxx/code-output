from src.updategebruiker_exceptions import *

class GebruikerService:
    def __init__(self, repository):
        self.repository = repository

    def update_gebruiker(self, gebruiker_id, nieuwe_gegevens):
        gebruiker = self.repository.get_by_id(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNietGevondenException()
        if not self._is_geldige_gegevens(nieuwe_gegevens):
            raise OngeldigeGebruikersgegevensException()
        if not self.mag_bewerken(gebruiker, nieuwe_gegevens):
            raise UpdateNietToegestaanException()
        self.repository.update(gebruiker_id, nieuwe_gegevens)
        gebruiker.update(nieuwe_gegevens)
        return gebruiker

    def mag_bewerken(self, gebruiker, nieuwe_gegevens):
        return True

    def _is_geldige_gegevens(self, gegevens):
        naam = gegevens.get("naam")
        email = gegevens.get("email")
        if not naam or not isinstance(naam, str):
            return False
        if not email or "@" not in email or not isinstance(email, str):
            return False
        return True
