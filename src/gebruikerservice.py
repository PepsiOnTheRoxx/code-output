class Gebruiker:
    def __init__(self, email, naam):
        if not self.is_valid_email(email):
            raise ValueError("Ongeldig emailadres.")
        self.email = email
        self.naam = naam

    @staticmethod
    def is_valid_email(email):
        return "@" in email

class GebruikerService:
    def create_gebruiker(self, email, naam):
        return Gebruiker(email, naam)

def main():
    pass

if __name__ == "__main__":
    main()