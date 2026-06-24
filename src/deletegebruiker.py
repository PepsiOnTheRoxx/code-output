class GebruikerNotFoundException(Exception):
    pass

class UserService:
    def __init__(self):
        self.gebruikers = {}

    def delete_gebruiker(self, gebruiker_id):
        if gebruiker_id not in self.gebruikers:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        del self.gebruikers[gebruiker_id]
        return True