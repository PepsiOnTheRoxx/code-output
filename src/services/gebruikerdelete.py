from src.services.gebruikerdelete_exceptions import (
    GebruikerDeleteException,
    GebruikerNietGevondenException,
    GebruikerDeleteNietToegestaanException,
    GebruikerDeleteDatabaseFoutException,
    GebruikerDeleteOnverwachteFoutException
)

class GebruikerNotFoundException(GebruikerNietGevondenException):
    pass

class GebruikerService:
    def verwijder_gebruiker(self, gebruiker_id):
        if not isinstance(gebruiker_id, int):
            raise TypeError("gebruiker_id moet een integer zijn")

        gebruiker = self._vind_gebruiker(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNotFoundException(f'Gebruiker met id {gebruiker_id} niet gevonden')
        self._verwijder_gebruiker(gebruiker)

    def _vind_gebruiker(self, gebruiker_id):
        raise NotImplementedError

    def _verwijder_gebruiker(self, gebruiker):
        raise NotImplementedError
