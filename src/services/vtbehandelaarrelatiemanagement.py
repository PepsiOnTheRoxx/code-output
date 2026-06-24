from src.services.vtbehandelaarrelatiemanagement_exceptions import (
    OngeldigeVernietigingstaakException,
    OngeldigeBehandelaarException,
    BehandelaarKoppelingBestaatAlException,
    BehandelaarKoppelingNietGevondenException,
)

class VTBehandelaarRelatie:
    def __init__(self, vernietigingstaak_id, gebruiker_id):
        self.vernietigingstaak_id = vernietigingstaak_id
        self.gebruiker_id = gebruiker_id

class VTBehandelaarRelatieService:
    def __init__(self):
        self._bestaande_vernietigingstaken = {1}
        self._bestaande_gebruikers = {10, 11}
        # relatie opslag: key=vernietigingstaak_id, value=set van gebruiker_id
        self._relaties = {}

    def koppel_behandelaar(self, vernietigingstaak_id, gebruiker_id):
        if vernietigingstaak_id not in self._bestaande_vernietigingstaken:
            raise OngeldigeVernietigingstaakException()
        if gebruiker_id not in self._bestaande_gebruikers:
            raise OngeldigeBehandelaarException()
        if vernietigingstaak_id not in self._relaties:
            self._relaties[vernietigingstaak_id] = set()
        if gebruiker_id in self._relaties[vernietigingstaak_id]:
            raise BehandelaarKoppelingBestaatAlException()
        self._relaties[vernietigingstaak_id].add(gebruiker_id)
        return VTBehandelaarRelatie(vernietigingstaak_id, gebruiker_id)

    def verwijder_behandelaar(self, vernietigingstaak_id, gebruiker_id):
        if vernietigingstaak_id not in self._bestaande_vernietigingstaken:
            raise OngeldigeVernietigingstaakException()
        if (
            vernietigingstaak_id not in self._relaties
            or gebruiker_id not in self._relaties[vernietigingstaak_id]
        ):
            raise BehandelaarKoppelingNietGevondenException()
        self._relaties[vernietigingstaak_id].remove(gebruiker_id)
        if not self._relaties[vernietigingstaak_id]:
            del self._relaties[vernietigingstaak_id]

    def lijst_behandelaars(self, vernietigingstaak_id):
        if vernietigingstaak_id not in self._bestaande_vernietigingstaken:
            raise OngeldigeVernietigingstaakException()
        relaties = []
        gebruiker_ids = self._relaties.get(vernietigingstaak_id, set())
        for gebruiker_id in gebruiker_ids:
            relaties.append(VTBehandelaarRelatie(vernietigingstaak_id, gebruiker_id))
        return relaties
