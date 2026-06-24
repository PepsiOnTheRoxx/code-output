from src.services.vtarchivarisrelatie_exceptions import (
    VTArchivarisRelatieAlreadyExistsException,
    VTArchivarisRelatieNotFoundException,
    VTArchivarisRelatieInvalidUserException,
    VTArchivarisRelatieInvalidTaakException,
)

class VTArchivarisRelatieOpslag:
    def __init__(self):
        # Opslag is een dict van gebruiker_id -> set van taak_ids
        self._relaties = {}

    def bestaat_relatie(self, gebruiker_id, taak_id):
        return (
            gebruiker_id in self._relaties and
            taak_id in self._relaties[gebruiker_id]
        )

    def opslaan_relatie(self, gebruiker_id, taak_id):
        if gebruiker_id not in self._relaties:
            self._relaties[gebruiker_id] = set()
        self._relaties[gebruiker_id].add(taak_id)

    def verwijder_relatie(self, gebruiker_id, taak_id):
        if gebruiker_id in self._relaties:
            self._relaties[gebruiker_id].discard(taak_id)
            if not self._relaties[gebruiker_id]:
                del self._relaties[gebruiker_id]

    def haal_taak_ids_voor_gebruiker(self, gebruiker_id):
        return list(self._relaties.get(gebruiker_id, set()))


class VTArchivarisRelatieService:
    def __init__(self):
        self.ops = VTArchivarisRelatieOpslag()

    def maak_relatie(self, gebruiker_id, taak_id):
        if not isinstance(gebruiker_id, int):
            raise VTArchivarisRelatieInvalidUserException()
        if not isinstance(taak_id, int):
            raise VTArchivarisRelatieInvalidTaakException()
        if self.ops.bestaat_relatie(gebruiker_id, taak_id):
            raise VTArchivarisRelatieAlreadyExistsException()
        self.ops.opslaan_relatie(gebruiker_id, taak_id)

    def verwijder_relatie(self, gebruiker_id, taak_id):
        if not self.ops.bestaat_relatie(gebruiker_id, taak_id):
            raise VTArchivarisRelatieNotFoundException()
        self.ops.verwijder_relatie(gebruiker_id, taak_id)

    def alle_relatie_ids_per_gebruiker(self, gebruiker_id):
        return self.ops.haal_taak_ids_voor_gebruiker(gebruiker_id)

    def bestaat_relatie(self, gebruiker_id, taak_id):
        return self.ops.bestaat_relatie(gebruiker_id, taak_id)
