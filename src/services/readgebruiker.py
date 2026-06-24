from src.services.readgebruiker_exceptions import GebruikerNotFoundException, InvalidGebruikerIdException

class GebruikerRepository:
    def get_gebruiker_by_id(self, gebruiker_id):
        raise NotImplementedError

class GebruikerService:
    def __init__(self):
        self.repository = GebruikerRepository()

    def read_gebruiker(self, gebruiker_id):
        if not isinstance(gebruiker_id, int):
            raise InvalidGebruikerIdException("Gegeven gebruiker_id is ongeldig")
        return self.repository.get_gebruiker_by_id(gebruiker_id)