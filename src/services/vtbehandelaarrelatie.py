from src.services.vtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieBestaatAlException,
    VTBehandelaarRelatieNietGevondenException,
    OngeldigeGebruikerException,
    OngeldigeVernietigingstaakException,
)

class VTBehandelaarRelatieService:
    _gebruikers = set([10, 11, 12, 15, 30, 31, 50, 70])
    _taken = set([20, 21, 22, 25, 40, 41, 60, 61])
    _relaties = set()  # Set van tuples (gebruiker_id, taak_id)

    def maak_relatie(self, gebruiker_id, taak_id):
        if not self.controleer_of_gebruiker_bestaat(gebruiker_id):
            raise OngeldigeGebruikerException()
        if not self.controleer_of_taak_bestaat(taak_id):
            raise OngeldigeVernietigingstaakException()
        if self.bestaat_relatie(gebruiker_id, taak_id):
            raise VTBehandelaarRelatieBestaatAlException()
        self.opslaan_relatie(gebruiker_id, taak_id)

    def verwijder_relatie(self, gebruiker_id, taak_id):
        if not self.bestaat_relatie(gebruiker_id, taak_id):
            raise VTBehandelaarRelatieNietGevondenException()
        self._verwijder_relatie(gebruiker_id, taak_id)

    def haal_relaties_op(self, gebruiker_id):
        if not self.controleer_of_gebruiker_bestaat(gebruiker_id):
            raise OngeldigeGebruikerException()
        return self.haal_relaties_op_voor_gebruiker(gebruiker_id)

    def controleer_of_gebruiker_bestaat(self, gebruiker_id):
        return gebruiker_id in self._gebruikers

    def controleer_of_taak_bestaat(self, taak_id):
        return taak_id in self._taken

    def bestaat_relatie(self, gebruiker_id, taak_id):
        return (gebruiker_id, taak_id) in self._relaties

    def opslaan_relatie(self, gebruiker_id, taak_id):
        self._relaties.add((gebruiker_id, taak_id))

    def _verwijder_relatie(self, gebruiker_id, taak_id):
        self._relaties.remove((gebruiker_id, taak_id))

    def haal_relaties_op_voor_gebruiker(self, gebruiker_id):
        return [
            {'gebruiker_id': gebruiker_id, 'taak_id': taak_id}
            for (gid, taak_id) in self._relaties if gid == gebruiker_id
        ]
