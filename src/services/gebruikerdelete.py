from src.services.gebruikerdelete_exceptions import (GebruikerBestaatNietException, VerwijderNietToegestaanException)

class GebruikerService:
    # Simuleer een database met gebruikers. In een echte implementatie zou dit een DB-call zijn.
    _gebruikers_db = {
        10: {'mag_verwijderen': True},
        20: {'mag_verwijderen': False},
        23: {'mag_verwijderen': False},
        42: {'mag_verwijderen': True},
        77: {'mag_verwijderen': True},
    }

    def verwijder(self, gebruiker_id):
        return self._verwijder_gebruiker(gebruiker_id)

    def _verwijder_gebruiker(self, gebruiker_id):
        gebruiker = self._gebruikers_db.get(gebruiker_id)
        if gebruiker is None:
            raise GebruikerBestaatNietException(f"Gebruiker met id {gebruiker_id} bestaat niet")
        if not gebruiker.get('mag_verwijderen', False):
            raise VerwijderNietToegestaanException(f"Niet toegestaan om gebruiker {gebruiker_id} te verwijderen")
        # Simuleer verwijderactie
        del self._gebruikers_db[gebruiker_id]
        return True
