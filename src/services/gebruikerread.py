from src.services.gebruikerread_exceptions import GebruikerNietGevondenException, OnbekendeFoutException

class GebruikerRepository:
    def get_gebruiker_by_id(self, gebruiker_id):
        pass

    def get_alle_gebruikers(self):
        pass

class GebruikerService:
    def __init__(self):
        self.repository = GebruikerRepository()

    def haal_gebruiker_op_by_id(self, gebruiker_id):
        try:
            gebruiker = self.repository.get_gebruiker_by_id(gebruiker_id)
            if gebruiker is None:
                raise GebruikerNietGevondenException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
            return gebruiker
        except GebruikerNietGevondenException:
            raise
        except Exception as e:
            raise OnbekendeFoutException(f"Onbekende fout bij ophalen gebruiker: {e}")

    def haal_alle_gebruikers(self):
        try:
            gebruikers = self.repository.get_alle_gebruikers()
            return gebruikers
        except Exception as e:
            raise OnbekendeFoutException(f"Onbekende fout bij ophalen alle gebruikers: {e}")