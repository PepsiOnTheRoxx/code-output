class GebruikerNotFoundException(Exception):
    pass

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}

    def add_gebruiker(self, gebruiker_id, naam, emailadres):
        self._gebruikers[gebruiker_id] = {"Naam": naam, "Emailadres": emailadres}

    def read_gebruiker(self, gebruiker_id):
        if gebruiker_id not in self._gebruikers:
            raise GebruikerNotFoundException()
        return self._gebruikers[gebruiker_id]