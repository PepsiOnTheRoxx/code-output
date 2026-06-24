class Gebruiker:
    _id_counter = 1

    def __init__(self, emailadres, naam):
        self.id = Gebruiker._id_counter
        Gebruiker._id_counter += 1
        self.emailadres = emailadres
        self.naam = naam

class GebruikerService:
    def __init__(self):
        self._gebruikers = {}

    def create_gebruiker(self, emailadres, naam):
        if emailadres is None or emailadres == '':
            raise ValueError("Emailadres ontbreekt")
        if naam is None or naam == '':
            raise ValueError("Naam ontbreekt")
        if not self._valid_email(emailadres):
            raise ValueError("Ongeldig e-mail formaat")
        if emailadres in self._gebruikers:
            raise ValueError("Emailadres bestaat al")
        gebruiker = Gebruiker(emailadres, naam)
        self._gebruikers[emailadres] = gebruiker
        return gebruiker

    def _valid_email(self, email):
        if not isinstance(email, str):
            return False
        if "@" not in email or "." not in email.split("@")[-1]:
            return False
        return True