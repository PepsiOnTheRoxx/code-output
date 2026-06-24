class GebruikerNotFoundException(Exception):
    pass

class Gebruiker:
    def __init__(self, gebruiker_id, naam, email):
        self.gebruiker_id = gebruiker_id
        self.naam = naam
        self.email = email

class GebruikerRepository:
    def __init__(self):
        self._gebruikers = {}

    def voeg_toe(self, gebruiker):
        self._gebruikers[gebruiker.gebruiker_id] = gebruiker

    def zoek_op_id(self, gebruiker_id):
        return self._gebruikers.get(gebruiker_id)

    def update(self, gebruiker_id, naam=None, email=None):
        gebruiker = self.zoek_op_id(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden")
        if naam is not None:
            gebruiker.naam = naam
        if email is not None:
            gebruiker.email = email
        return gebruiker

class UserService:
    def __init__(self, gebruiker_repository):
        self.gebruiker_repository = gebruiker_repository

    def update_gebruiker(self, gebruiker_id, naam=None, email=None):
        return self.gebruiker_repository.update(gebruiker_id, naam=naam, email=email)