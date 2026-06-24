class Gebruiker:
    def __init__(self, gebruikersnaam, email):
        if not gebruikersnaam or not email:
            raise ValueError("Gebruikersnaam en email zijn verplicht.")
        self.gebruikersnaam = gebruikersnaam
        self.email = email


class GebruikerBestaatAlException(Exception):
    pass


class GebruikerBestaatNietException(Exception):
    pass


class UserService:
    def __init__(self):
        self.gebruikers = []

    def create_gebruiker(self, gebruikersnaam, email):
        gebruiker = Gebruiker(gebruikersnaam, email)
        self.gebruikers.append(gebruiker)
        return gebruiker

    def get_gebruikers(self):
        return self.gebruikers

    def update_gebruiker(self, oude_gebruikersnaam, new_gebruikersnaam=None, new_email=None):
        gebruiker = next((g for g in self.gebruikers if g.gebruikersnaam == oude_gebruikersnaam), None)
        if gebruiker is None:
            raise GebruikerBestaatNietException(f"GEBRUIKER MET GEBRUIKERSNAAM '{oude_gebruikersnaam}' BESTAAT NIET")

        if new_gebruikersnaam:
            if any(g.gebruikersnaam == new_gebruikersnaam for g in self.gebruikers):
                raise GebruikerBestaatAlException(f"GEBRUIKER MET GEBRUIKERSNAAM '{new_gebruikersnaam}' BESTAAT AL")
            gebruiker.gebruikersnaam = new_gebruikersnaam

        if new_email:
            gebruiker.email = new_email
        return gebruiker

    def delete_gebruiker(self, gebruikersnaam):
        gebruiker = next((g for g in self.gebruikers if g.gebruikersnaam == gebruikersnaam), None)
        if gebruiker is None:
            raise GebruikerBestaatNietException(f"GEBRUIKER MET GEBRUIKERSNAAM '{gebruikersnaam}' BESTAAT NIET")
        self.gebruikers.remove(gebruiker)