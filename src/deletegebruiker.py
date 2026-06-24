from src.deletegebruiker_exceptions import *

class GebruikerService:
    def verwijder_gebruiker(self, gebruiker_id):
        if not self.bestaat_gebruiker(gebruiker_id):
            raise GebruikerNietGevondenException()
        if not self.mag_verwijderen(gebruiker_id):
            raise GebruikerVerwijderenNietToegestaanException()
        try:
            self.verwijder_gebruiker_uit_db(gebruiker_id)
        except GebruikerDeleteDatabaseFoutException:
            raise
    def bestaat_gebruiker(self, gebruiker_id):
        raise NotImplementedError()

    def mag_verwijderen(self, gebruiker_id):
        raise NotImplementedError()

    def verwijder_gebruiker_uit_db(self, gebruiker_id):
        raise NotImplementedError()
