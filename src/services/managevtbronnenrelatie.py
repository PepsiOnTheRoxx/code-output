from src.services.managevtbronnenrelatie_exceptions import (
    VTBronnenRelatieNotFoundException,
    VTBronnenRelatieAlreadyExistsException,
    VTBronnenRelatieUpdateException
)

class VTBronnenRelatieRepository:
    def exists(self, vernietigingstaak_id, bron_id):
        # Implementatie van de persistence laag. Wordt gemocked in tests.
        raise NotImplementedError

    def add(self, vernietigingstaak_id, bron_id):
        raise NotImplementedError

    def delete(self, vernietigingstaak_id, bron_id):
        raise NotImplementedError

    def update(self, vernietigingstaak_id, bron_id, nieuwe_bron_id):
        raise NotImplementedError

    def get_bronnen_by_taak(self, vernietigingstaak_id):
        raise NotImplementedError

class VTBronnenRelatieService:
    def __init__(self):
        self._repo = VTBronnenRelatieRepository()

    def create_relatie(self, vernietigingstaak_id, bron_id):
        if self._repo.exists(vernietigingstaak_id=vernietigingstaak_id, bron_id=bron_id):
            raise VTBronnenRelatieAlreadyExistsException()
        self._repo.add(vernietigingstaak_id=vernietigingstaak_id, bron_id=bron_id)
        return True

    def delete_relatie(self, vernietigingstaak_id, bron_id):
        if not self._repo.exists(vernietigingstaak_id=vernietigingstaak_id, bron_id=bron_id):
            raise VTBronnenRelatieNotFoundException()
        self._repo.delete(vernietigingstaak_id=vernietigingstaak_id, bron_id=bron_id)
        return True

    def update_relatie(self, vernietigingstaak_id, bron_id, nieuwe_bron_id):
        if not self._repo.exists(vernietigingstaak_id=vernietigingstaak_id, bron_id=bron_id):
            raise VTBronnenRelatieNotFoundException()
        return self._repo.update(vernietigingstaak_id=vernietigingstaak_id, bron_id=bron_id, nieuwe_bron_id=nieuwe_bron_id) or True

    def get_bronnen_by_taak(self, vernietigingstaak_id):
        return self._repo.get_bronnen_by_taak(vernietigingstaak_id=vernietigingstaak_id)
