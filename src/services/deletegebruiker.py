from src.services.deletegebruiker_exceptions import GebruikerNietGevondenException, DeleteGebruikerException

class GebruikerRepository:
    def gebruiker_bestaat(self, gebruiker_id):
        # Dummy: override in practice, pretend that gebruiker exists if ID is integer and >= 0
        return type(gebruiker_id) is int and gebruiker_id >= 0

    def verwijder_gebruiker(self, gebruiker_id):
        # Dummy: override with echte database logica
        return True

class GebruikerService:
    def __init__(self):
        self.repository = GebruikerRepository()

    def verwijder_gebruiker(self, gebruiker_id):
        try:
            if not self.repository.gebruiker_bestaat(gebruiker_id):
                raise GebruikerNietGevondenException()
            success = self.repository.verwijder_gebruiker(gebruiker_id)
            if not success:
                raise DeleteGebruikerException("Verwijderen van gebruiker is niet geslaagd.")
            return True
        except GebruikerNietGevondenException:
            raise
        except DeleteGebruikerException:
            raise
        except Exception as e:
            raise DeleteGebruikerException(str(e))
