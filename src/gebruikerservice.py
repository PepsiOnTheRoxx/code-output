class GebruikerNietGevondenFout(Exception):
    pass

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}

    def voeg_gebruiker_toe(self, gebruiker_id, naam, email):
        self._gebruikers[gebruiker_id] = {
            "naam": naam,
            "email": email
        }

    def verwijder_gebruiker(self, gebruiker_id):
        if not gebruiker_id or gebruiker_id not in self._gebruikers:
            raise GebruikerNietGevondenFout()
        del self._gebruikers[gebruiker_id]

    def bestaat_gebruiker(self, gebruiker_id):
        return gebruiker_id in self._gebruikers