from src.services.vtbronnenrelatie_exceptions import (
    BronNotFoundException,
    VernietigingstaakNotFoundException,
    RelatieBestaatAlException,
)

# Simpele in-memory opslag voor bron, taak en relaties
__BRONNEN = {}
__TAKEN = {}
__RELATIES = set()  # Set van tuples (bron_id, taak_id)

def reset_stores():
    global __BRONNEN, __TAKEN, __RELATIES
    __BRONNEN.clear()
    __TAKEN.clear()
    __RELATIES.clear()

class BronRepository:
    def get_by_id(self, bron_id):
        return __BRONNEN.get(bron_id)

    def save(self, bron):
        __BRONNEN[bron['id']] = bron
        return bron

class VernietigingstaakRepository:
    def get_by_id(self, taak_id):
        return __TAKEN.get(taak_id)

    def save(self, taak):
        __TAKEN[taak['id']] = taak
        return taak

class RelatieRepository:
    def get_by_bron_en_taak(self, bron_id, taak_id):
        if (bron_id, taak_id) in __RELATIES:
            # Iets simpels als representatie
            return {'bron_id': bron_id, 'taak_id': taak_id}
        return None

    def create(self, bron_id, taak_id):
        __RELATIES.add((bron_id, taak_id))
        return {'bron_id': bron_id, 'taak_id': taak_id}

    def delete_by_bron_en_taak(self, bron_id, taak_id):
        if (bron_id, taak_id) in __RELATIES:
            __RELATIES.remove((bron_id, taak_id))
            return True
        return False

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
