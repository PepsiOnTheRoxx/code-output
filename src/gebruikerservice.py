class Gebruiker:
    def __init__(self, naam, email):
        self.naam = naam
        self.email = email


class GebruikerService:
    def __init__(self):
        self.gebruikers = []

    def creeer_gebruiker(self, gebruiker_data):
        naam = gebruiker_data.get("naam")
        email = gebruiker_data.get("email")

        if not naam:
            raise ValueError("Naam is verplicht")
        if not email:
            raise ValueError("Email is verplicht")
        if not self.is_valid_email(email):
            raise ValueError("Ongeldig emailadres")
        if any(gebruiker.email == email for gebruiker in self.gebruikers):
            raise ValueError("Email moet uniek zijn")

        gebruiker = Gebruiker(naam, email)
        self.gebruikers.append(gebruiker)
        return gebruiker

    def is_valid_email(self, email):
        return "@" in email and "." in email.split("@")[-1]