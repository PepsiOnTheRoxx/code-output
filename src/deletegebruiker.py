from src.deletegebruiker_exceptions import *

class GebruikerService:
    def verwijder_gebruiker(self, gebruiker_id):
        if not self.bestaat_gebruiker(gebruiker_id):
            raise GebruikerNotFound()
        if not self.mag_verwijderen(gebruiker_id):
            raise UnauthorizedOperation()
        try:
            self.verwijder_gebruiker_uit_db(gebruiker_id)
        except GebruikerDeleteError:
            raise
    def bestaat_gebruiker(self, gebruiker_id):
        raise NotImplementedError()

    def mag_verwijderen(self, gebruiker_id):
        raise NotImplementedError()

    def verwijder_gebruiker_uit_db(self, gebruiker_id):
        raise NotImplementedError()