from src.services.vtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieBestaatAlException,
    VTBehandelaarRelatieNietGevondenException,
    OngeldigeGebruikerException,
    OngeldigeVernietigingstaakException,
)

class VTBehandelaarRelatieService:
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

    # Methoden hieronder zijn placeholders/wrappers voor daadwerkelijke implementaties.
    def controleer_of_gebruiker_bestaat(self, gebruiker_id):
        raise NotImplementedError()

    def controleer_of_taak_bestaat(self, taak_id):
        raise NotImplementedError()

    def bestaat_relatie(self, gebruiker_id, taak_id):
        raise NotImplementedError()

    def opslaan_relatie(self, gebruiker_id, taak_id):
        raise NotImplementedError()

    def _verwijder_relatie(self, gebruiker_id, taak_id):
        raise NotImplementedError()

    def haal_relaties_op_voor_gebruiker(self, gebruiker_id):
        raise NotImplementedError()
