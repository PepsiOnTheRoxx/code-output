from src.readgebruiker_exceptions import *

class GebruikerService:
    def __init__(self, repo):
        self.repo = repo

    def read_gebruiker(self, gebruiker_id):
        if not isinstance(gebruiker_id, int):
            raise OngeldigeGebruikerIDException()
        gebruiker = self.repo.get_gebruiker_by_id(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNietGevondenException()
        return {
            'id': gebruiker.get('id'),
            'naam': gebruiker.get('naam'),
            'email': gebruiker.get('email')
        }
