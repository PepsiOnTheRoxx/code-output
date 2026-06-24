class GebruikerNotFoundException(Exception):
    pass

class UserService:
    def __init__(self, gebruiker_data):
        # gebruiker_data is a list of dicts with keys: id, naam, email
        self._gebruikers = {}
        for g in gebruiker_data:
            self._gebruikers[g["id"]] = dict(g)  # make a shallow copy

    def read_gebruiker(self, gebruiker_id):
        if not isinstance(gebruiker_id, int):
            raise TypeError("gebruiker_id moet een integer zijn")
        if gebruiker_id not in self._gebruikers:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        # Return a COPY, not the reference
        return dict(self._gebruikers[gebruiker_id])