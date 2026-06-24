from src.services.gebruikerread_exceptions import GebruikerNietGevondenException

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}

    def lees_gebruiker(self, gebruiker_id):
        if type(gebruiker_id) is not int or gebruiker_id is None or gebruiker_id not in self._gebruikers or gebruiker_id <= 0:
            raise GebruikerNietGevondenException()
        return self._gebruikers[gebruiker_id]