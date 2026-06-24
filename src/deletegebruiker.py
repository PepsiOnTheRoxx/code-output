class GebruikerNietGevondenException(Exception):
    pass

class Gebruiker:
    def __init__(self, gebruiker_id, naam):
        self.gebruiker_id = gebruiker_id
        self.naam = naam

class GebruikerRepository:
    def __init__(self):
        self._gebruikers = {}  # gebruiker_id -> Gebruiker

    def save(self, gebruiker):
        self._gebruikers[gebruiker.gebruiker_id] = gebruiker

    def find_by_id(self, gebruiker_id):
        return self._gebruikers.get(gebruiker_id, None)

    def delete(self, gebruiker_id):
        if gebruiker_id in self._gebruikers:
            del self._gebruikers[gebruiker_id]
            return True
        return False

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def delete_gebruiker(self, gebruiker_id):
        gebruiker = self.repository.find_by_id(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNietGevondenException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        self.repository.delete(gebruiker_id)
        return True