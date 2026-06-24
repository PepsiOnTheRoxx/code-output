from src.services.readgebruiker_exceptions import GebruikerNotFoundException, GebruikerInvalidInputException

class GebruikerRepository:
    # Dummy in-memory database for demonstration
    _fake_db = {
        123: {
            'id': 123, 'naam': 'Jan Jansen', 'email': 'jan.jansen@example.com', 'active': True
        },
        42: {
            'id': 42, 'naam': 'Jane Doe', 'email': 'jane.doe@example.com', 'active': False
        }
    }

    def get_gebruiker_by_id(self, gebruiker_id):
        if gebruiker_id in self._fake_db:
            return self._fake_db[gebruiker_id]
        else:
            raise GebruikerNotFoundException(f'Gebruiker met id {gebruiker_id} niet gevonden')

class GebruikerService:
    def __init__(self):
        self.repository = GebruikerRepository()

    def read_gebruiker(self, gebruiker_id):
        if not isinstance(gebruiker_id, int):
            raise GebruikerInvalidInputException("Gegeven gebruiker_id is ongeldig")
        return self.repository.get_gebruiker_by_id(gebruiker_id)
