class Gebruiker:
    def __init__(self, gebruiker_id, naam):
        self.gebruiker_id = gebruiker_id
        self.naam = naam

class GebruikerNotFoundException(Exception):
    pass

class UserService:
    def __init__(self):
        self._gebruikers = {}

    def add_gebruiker(self, gebruiker_id, naam):
        gebruiker = Gebruiker(gebruiker_id, naam)
        self._gebruikers[gebruiker_id] = gebruiker

    def read_gebruiker(self, gebruiker_id):
        if gebruiker_id in self._gebruikers:
            return self._gebruikers[gebruiker_id]
        else:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")