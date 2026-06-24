from src.services.gebruikerdelete_exceptions import GebruikerBestaatNietException, VerwijderNietToegestaanException

class GebruikerService:
    def verwijder(self, gebruiker_id):
        return self._verwijder_gebruiker(gebruiker_id)

    def _verwijder_gebruiker(self, gebruiker_id):
        # Dummy implementatie (voor test). Gooi nooit errors hier.
        return True
