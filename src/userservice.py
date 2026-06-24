from email.utils import parseaddr

class Gebruiker:
    def __init__(self, gebruikersnaam, email, wachtwoord):
        self.gebruikersnaam = gebruikersnaam
        self.email = email
        self.wachtwoord = self.encrypt_wachtwoord(wachtwoord)

    def encrypt_wachtwoord(self, wachtwoord):
        return f"encrypted({wachtwoord})"


class UserService:
    def __init__(self):
        self.gebruikers = {}

    def create_gebruiker(self, gebruiker_data):
        if 'gebruikersnaam' not in gebruiker_data or 'email' not in gebruiker_data or 'wachtwoord' not in gebruiker_data:
            raise ValueError('Missing required gebruiker information')

        gebruikersnaam = gebruiker_data['gebruikersnaam']
        email = gebruiker_data['email']
        wachtwoord = gebruiker_data['wachtwoord']

        if not self.is_valid_email(email):
            raise ValueError('Invalid email format')

        if gebruikersnaam in self.gebruikers:
            raise ValueError('Gebruiker already exists')

        gebruiker = Gebruiker(gebruikersnaam, email, wachtwoord)
        self.gebruikers[gebruikersnaam] = gebruiker
        return gebruiker

    def is_valid_email(self, email):
        return "@" in parseaddr(email)[1] and '.' in parseaddr(email)[1]