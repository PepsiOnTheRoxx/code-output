from src.services.gebruikerdelete_exceptions import GebruikerBestaatNietException, VerwijderNietToegestaanException

class GebruikerService:
    def verwijder(self, gebruiker_id):
        return self._verwijder_gebruiker(gebruiker_id)

    def _verwijder_gebruiker(self, gebruiker_id):
        # Deze methode moet worden geïmplementeerd met logica voor het verwijderen van een gebruiker.
        # In deze stub raise of return, afhankelijk van implementatie in unit test.
        raise NotImplementedError