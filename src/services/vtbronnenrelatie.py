from src.services.vtbronnenrelatie_exceptions import (
    BronNotFoundException,
    VernietigingstaakNotFoundException,
    RelatieBestaatAlException,
)

class BronRepository:
    def get_by_id(self, bron_id):
        pass

class VernietigingstaakRepository:
    def get_by_id(self, taak_id):
        pass

class RelatieRepository:
    def get_by_bron_en_taak(self, bron_id, taak_id):
        pass

    def create(self, bron_id, taak_id):
        pass

    def delete_by_bron_en_taak(self, bron_id, taak_id):
        pass

class VTBronnenRelatieService:
    def __init__(self):
        self.bron_repo = BronRepository()
        self.vernietigingstaak_repo = VernietigingstaakRepository()
        self.relatie_repo = RelatieRepository()

    def koppel_bron_aan_vernietigingstaak(self, bron_id, taak_id):
        bron = self.bron_repo.get_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden.")

        taak = self.vernietigingstaak_repo.get_by_id(taak_id)
        if taak is None:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")

        relatie = self.relatie_repo.get_by_bron_en_taak(bron_id, taak_id)
        if relatie is not None:
            raise RelatieBestaatAlException(f"Relatie tussen bron {bron_id} en taak {taak_id} bestaat al.")

        self.relatie_repo.create(bron_id, taak_id)

    def verwijder_relatie(self, bron_id, taak_id):
        result = self.relatie_repo.delete_by_bron_en_taak(bron_id, taak_id)
        return result

    def haal_op_relatie(self, bron_id, taak_id):
        relatie = self.relatie_repo.get_by_bron_en_taak(bron_id, taak_id)
        return relatie
