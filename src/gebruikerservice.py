class Gebruiker:
    def __init__(self, id, naam, email):
        self.id = id
        self.naam = naam
        self.email = email

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}

    def add_gebruiker(self, gebruiker):
        self._gebruikers[gebruiker.id] = gebruiker

    def update_gebruiker(self, gebruiker_id, updated_data):
        if gebruiker_id not in self._gebruikers:
            raise KeyError("Gebruiker niet gevonden")
        gebruiker = self._gebruikers[gebruiker_id]
        allowed_attrs = ("naam", "email")
        for attr in updated_data:
            if attr not in allowed_attrs:
                raise AttributeError(f"Attribute '{attr}' mag niet gewijzigd worden")
            setattr(gebruiker, attr, updated_data[attr])
        return gebruiker