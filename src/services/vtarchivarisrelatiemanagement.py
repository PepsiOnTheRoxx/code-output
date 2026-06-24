from src.services.vtarchivarisrelatiemanagement_exceptions import (
    RelatieBestaatAlException,
    RelatieNietGevondenException,
    OngeldigeInputException
)

class VTArchivarisRelatieService:
    def __init__(self):
        self._relaties = {}
    
    def voeg_relatie_toe(self, vernietigingstaak_id, gebruiker_id):
        if vernietigingstaak_id is None or gebruiker_id is None:
            raise OngeldigeInputException("vernietigingstaak_id en gebruiker_id mogen niet None zijn")
        if vernietigingstaak_id not in self._relaties:
            self._relaties[vernietigingstaak_id] = set()
        if gebruiker_id in self._relaties[vernietigingstaak_id]:
            raise RelatieBestaatAlException("Relatie bestaat al")
        self._relaties[vernietigingstaak_id].add(gebruiker_id)
    
    def verwijder_relatie(self, vernietigingstaak_id, gebruiker_id):
        if vernietigingstaak_id is None or gebruiker_id is None:
            raise OngeldigeInputException("vernietigingstaak_id en gebruiker_id mogen niet None zijn")
        if vernietigingstaak_id not in self._relaties:
            raise RelatieNietGevondenException("Geen relaties gevonden voor deze vernietigingstaak")
        if gebruiker_id not in self._relaties[vernietigingstaak_id]:
            raise RelatieNietGevondenException("Relatie niet gevonden")
        self._relaties[vernietigingstaak_id].remove(gebruiker_id)
        if not self._relaties[vernietigingstaak_id]:
            del self._relaties[vernietigingstaak_id]
    
    def lijst_relaties(self, vernietigingstaak_id):
        if vernietigingstaak_id is None:
            raise OngeldigeInputException("vernietigingstaak_id mag niet None zijn")
        return list(self._relaties.get(vernietigingstaak_id, []))