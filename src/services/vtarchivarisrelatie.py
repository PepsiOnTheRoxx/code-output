from src.services.vtarchivarisrelatie_exceptions import (
    ArchivarisRelatieAlreadyExistsException,
    ArchivarisRelatieNotFoundException,
    InvalidGebruikerException,
    InvalidVernietigingstaakException,
)
from src.services.vtarchivarisrelatie import VTArchivarisRelatieOpslag


class VTArchivarisRelatieService:
    def __init__(self):
        self.ops = VTArchivarisRelatieOpslag()

    def maak_relatie(self, gebruiker_id, taak_id):
        if not isinstance(gebruiker_id, int):
            raise InvalidGebruikerException()
        if not isinstance(taak_id, int):
            raise InvalidVernietigingstaakException()
        if self.ops.bestaat_relatie(gebruiker_id, taak_id):
            raise ArchivarisRelatieAlreadyExistsException()
        self.ops.opslaan_relatie(gebruiker_id, taak_id)

    def verwijder_relatie(self, gebruiker_id, taak_id):
        if not self.ops.bestaat_relatie(gebruiker_id, taak_id):
            raise ArchivarisRelatieNotFoundException()
        self.ops.verwijder_relatie(gebruiker_id, taak_id)

    def alle_relatie_ids_per_gebruiker(self, gebruiker_id):
        return self.ops.haal_taak_ids_voor_gebruiker(gebruiker_id)

    def bestaat_relatie(self, gebruiker_id, taak_id):
        return self.ops.bestaat_relatie(gebruiker_id, taak_id)