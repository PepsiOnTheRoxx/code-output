class VTBehandelaarRelationException(Exception):
    pass

class Gebruiker:
    def __init__(self, id, naam):
        self.id = id
        self.naam = naam

    def __eq__(self, other):
        return isinstance(other, Gebruiker) and self.id == other.id and self.naam == other.naam

    def __hash__(self):
        return hash((self.id, self.naam))

class Vernietigingstaak:
    def __init__(self, id, omschrijving):
        self.id = id
        self.omschrijving = omschrijving

    def __eq__(self, other):
        return isinstance(other, Vernietigingstaak) and self.id == other.id and self.omschrijving == other.omschrijving

    def __hash__(self):
        return hash((self.id, self.omschrijving))

class DestructionTaskService:
    def __init__(self):
        # mapping: taak_id -> set van gebruikers (Gebruiker instanties)
        self._taak_to_gebruikers = {}
        # mapping: gebruiker_id -> set van taken (Vernietigingstaak instanties)
        self._gebruiker_to_taken = {}

    def koppel_behandelaar(self, gebruiker, taak):
        if not isinstance(gebruiker, Gebruiker):
            raise VTBehandelaarRelationException("Behandelaar is geen Gebruiker instantie")
        if not isinstance(taak, Vernietigingstaak):
            raise VTBehandelaarRelationException("Taak is geen Vernietigingstaak instantie")

        if taak.id not in self._taak_to_gebruikers:
            self._taak_to_gebruikers[taak.id] = set()
        # Check of gebruiker al gekoppeld is aan deze taak
        if gebruiker in self._taak_to_gebruikers[taak.id]:
            raise VTBehandelaarRelationException("Deze behandelaar is al gekoppeld aan deze taak")
        self._taak_to_gebruikers[taak.id].add(gebruiker)

        if gebruiker.id not in self._gebruiker_to_taken:
            self._gebruiker_to_taken[gebruiker.id] = set()
        self._gebruiker_to_taken[gebruiker.id].add(taak)
        return True

    def ontkoppel_behandelaar(self, gebruiker, taak):
        if not isinstance(gebruiker, Gebruiker):
            raise VTBehandelaarRelationException("Behandelaar is geen Gebruiker instantie")
        if not isinstance(taak, Vernietigingstaak):
            raise VTBehandelaarRelationException("Taak is geen Vernietigingstaak instantie")

        if taak.id not in self._taak_to_gebruikers or gebruiker not in self._taak_to_gebruikers[taak.id]:
            raise VTBehandelaarRelationException("Behandelaar is niet gekoppeld aan deze taak")
        self._taak_to_gebruikers[taak.id].remove(gebruiker)
        if not self._taak_to_gebruikers[taak.id]:
            del self._taak_to_gebruikers[taak.id]
        self._gebruiker_to_taken[gebruiker.id].remove(taak)
        if not self._gebruiker_to_taken[gebruiker.id]:
            del self._gebruiker_to_taken[gebruiker.id]
        return True

    def is_behandelaar(self, gebruiker, taak):
        if not isinstance(gebruiker, Gebruiker):
            return False
        if not isinstance(taak, Vernietigingstaak):
            return False
        return taak.id in self._taak_to_gebruikers and gebruiker in self._taak_to_gebruikers[taak.id]

    def get_behandelaars(self, taak):
        if not isinstance(taak, Vernietigingstaak):
            raise VTBehandelaarRelationException("Taak is geen Vernietigingstaak instantie")
        if taak.id in self._taak_to_gebruikers:
            return set(self._taak_to_gebruikers[taak.id])
        return set()

    def get_taken(self, gebruiker):
        if not isinstance(gebruiker, Gebruiker):
            raise VTBehandelaarRelationException("Behandelaar is geen Gebruiker instantie")
        if gebruiker.id in self._gebruiker_to_taken:
            return set(self._gebruiker_to_taken[gebruiker.id])
        return set()