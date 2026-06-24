class Gebruiker:
    def __init__(self, gebruikersnaam, email):
        self.gebruikersnaam = gebruikersnaam
        self.email = email


class UserService:
    def __init__(self):
        self.gebruikers = {}

    def create_gebruiker(self, gebruikersnaam, email):
        if gebruikersnaam in self.gebruikers:
            raise GebruikerBestaatAlException(f"GEBRUIKER MET GEBRUIKERSNAAM '{gebruikersnaam}' BESTAAT AL")
        gebruiker = Gebruiker(gebruikersnaam, email)
        self.gebruikers[gebruikersnaam] = gebruiker
        return gebruiker

    def get_gebruiker(self, gebruikersnaam):
        return self.gebruikers.get(gebruikersnaam)

    def update_gebruiker(self, gebruikersnaam, new_gebruikersnaam=None, new_email=None):
        gebruiker = self.get_gebruiker(gebruikersnaam)
        if not gebruiker:
            raise GebruikerBestaatNietException(f"GEBRUIKER MET GEBRUIKERSNAAM '{gebruikersnaam}' BESTAAT NIET")

        if new_gebruikersnaam:
            if new_gebruikersnaam in self.gebruikers and new_gebruikersnaam != gebruikersnaam:
                raise GebruikerBestaatAlException(f"GEBRUIKER MET GEBRUIKERSNAAM '{new_gebruikersnaam}' BESTAAT AL")
            gebruiker.gebruikersnaam = new_gebruikersnaam

        if new_email:
            gebruiker.email = new_email
        return gebruiker

    def delete_gebruiker(self, gebruikersnaam):
        if gebruikersnaam not in self.gebruikers:
            raise GebruikerBestaatNietException(f"GEBRUIKER MET GEBRUIKERSNAAM '{gebruikersnaam}' BESTAAT NIET")
        del self.gebruikers[gebruikersnaam]


class GebruikerBestaatAlException(Exception):
    pass


class GebruikerBestaatNietException(Exception):
    pass