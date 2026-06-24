from src.services.managevtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieAlreadyExists,
    VTBehandelaarRelatieNotFound,
    InvalidVTBehandelaarRelatieData,
)

class VTBehandelaarRelatieService:
    def __init__(self):
        # interne representatie als {(gebruiker_id, vernietigingstaak_id): True}
        self._relaties = {}
        # indexen voor snel zoeken
        self._taak_to_behandelaars = {}
        self._behandelaar_to_taken = {}

    def voeg_behandelaar_toe(self, gebruiker_id, vernietigingstaak_id):
        if not self._is_geldige_behandelaar(gebruiker_id):
            raise InvalidVTBehandelaarRelatieData()

        key = (gebruiker_id, vernietigingstaak_id)
        if key in self._relaties:
            raise VTBehandelaarRelatieAlreadyExists()

        self._relaties[key] = True
        self._taak_to_behandelaars.setdefault(vernietigingstaak_id, set()).add(gebruiker_id)
        self._behandelaar_to_taken.setdefault(gebruiker_id, set()).add(vernietigingstaak_id)
        return True

    def verwijder_behandelaar(self, gebruiker_id, vernietigingstaak_id):
        key = (gebruiker_id, vernietigingstaak_id)
        if key not in self._relaties:
            raise VTBehandelaarRelatieNotFound()

        del self._relaties[key]
        if vernietigingstaak_id in self._taak_to_behandelaars:
            self._taak_to_behandelaars[vernietigingstaak_id].discard(gebruiker_id)
            if not self._taak_to_behandelaars[vernietigingstaak_id]:
                del self._taak_to_behandelaars[vernietigingstaak_id]
        if gebruiker_id in self._behandelaar_to_taken:
            self._behandelaar_to_taken[gebruiker_id].discard(vernietigingstaak_id)
            if not self._behandelaar_to_taken[gebruiker_id]:
                del self._behandelaar_to_taken[gebruiker_id]
        return True

    def get_behandelaars_by_taak(self, vernietigingstaak_id):
        return list(self._taak_to_behandelaars.get(vernietigingstaak_id, set()))

    def get_taken_by_behandelaar(self, gebruiker_id):
        return list(self._behandelaar_to_taken.get(gebruiker_id, set()))

    def _is_geldige_behandelaar(self, gebruiker_id):
        # Dummy validatie: alle gebruiker_ids kleiner dan 90 zijn geldig
        return isinstance(gebruiker_id, int) and gebruiker_id < 90
