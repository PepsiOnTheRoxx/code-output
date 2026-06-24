from src.services.brondelete_exceptions import BronNotFoundException, BronDeleteException

# Simulatie van een eenvoudige Bron-database voor deze implementatie
db = {
    1: {"name": "Bron 1", "in_use": False, "state": "active"},
    2: {"name": "Bron 2", "in_use": False, "state": "active"},
    3: {"name": "Bron 3", "in_use": False, "state": "active"},
}

class BronService:
    def bron_exists(self, bron_id):
        # Controleer of bron bestaat in onze gesimuleerde database
        return bron_id in db

    def delete_bron(self, bron_id):
        # Probeer bron te verwijderen uit onze gesimuleerde database
        if bron_id not in db:
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden")
        del db[bron_id]

    def delete(self, bron_id):
        if not self.bron_exists(bron_id):
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden")
        self.delete_bron(bron_id)
