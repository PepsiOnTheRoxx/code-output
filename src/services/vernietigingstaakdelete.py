from src.services.vernietigingstaakdelete_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakDeleteException
)

class VernietigingstaakService:
    def get_by_id(self, taak_id):
        """
        Haal een Vernietigingstaak op uit de datastore op basis van het ID.
        Implementeer deze methode afhankelijk van de datastore.
        """
        raise NotImplementedError

    def delete_by_id(self, taak_id):
        """
        Verwijder een Vernietigingstaak uit de datastore op basis van het ID.
        Implementeer deze methode afhankelijk van de datastore.
        """
        raise NotImplementedError

    def delete_vernietigingstaak(self, taak_id):
        try:
            taak = self.get_by_id(taak_id)
        except VernietigingstaakNotFoundException:
            raise
        self.delete_by_id(taak_id)