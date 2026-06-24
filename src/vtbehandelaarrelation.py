class Gebruiker:
    def __init__(self, gebruiker_id, naam):
        self.gebruiker_id = gebruiker_id
        self.naam = naam

class Vernietigingstaak:
    def __init__(self, taak_id, beschrijving):
        self.taak_id = taak_id
        self.beschrijving = beschrijving

class VTBehandelaarRelationError(Exception):
    pass

class VTBehandelaarRelation:
    def __init__(self):
        # Key: Vernietigingstaak.taak_id, Value: Gebruiker.gebruiker_id
        self._relaties = dict()
        # Houdt instanties bij zodat teruggegeven instanties origineel zijn
        self._gebruikers = dict()
        self._taken = dict()

    def koppel_behandelaar(self, gebruiker, vernietigingstaak):
        if not isinstance(gebruiker, Gebruiker):
            raise VTBehandelaarRelationError("Behandelaar is geen Gebruiker instantie")
        if not isinstance(vernietigingstaak, Vernietigingstaak):
            raise VTBehandelaarRelationError("Taak is geen Vernietigingstaak instantie")
        if vernietigingstaak.taak_id in self._relaties:
            raise VTBehandelaarRelationError("Taak heeft al een behandelaar")
        self._relaties[vernietigingstaak.taak_id] = gebruiker.gebruiker_id
        self._gebruikers[gebruiker.gebruiker_id] = gebruiker
        self._taken[vernietigingstaak.taak_id] = vernietigingstaak

    def ontkoppel_behandelaar(self, vernietigingstaak):
        if not isinstance(vernietigingstaak, Vernietigingstaak):
            raise VTBehandelaarRelationError("Taak is geen Vernietigingstaak instantie")
        taak_id = vernietigingstaak.taak_id
        if taak_id not in self._relaties:
            raise VTBehandelaarRelationError("Taak heeft geen behandelaar gekoppeld")
        del self._relaties[taak_id]
        # Schoon verder netjes op als taak niet meer bestaat
        del self._taken[taak_id]

    def get_behandelaar(self, vernietigingstaak):
        if not isinstance(vernietigingstaak, Vernietigingstaak):
            raise VTBehandelaarRelationError("Taak is geen Vernietigingstaak instantie")
        taak_id = vernietigingstaak.taak_id
        if taak_id not in self._relaties:
            return None
        gebruiker_id = self._relaties[taak_id]
        gebruiker = self._gebruikers.get(gebruiker_id)
        return gebruiker

    def get_taak(self, gebruiker):
        if not isinstance(gebruiker, Gebruiker):
            raise VTBehandelaarRelationError("Gebruiker is geen Gebruiker instantie")
        gebruikers_id = gebruiker.gebruiker_id
        for taak_id, gebruiker_id in self._relaties.items():
            if gebruiker_id == gebruikers_id:
                return self._taken[taak_id]
        return None