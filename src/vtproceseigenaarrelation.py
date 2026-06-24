class ProceseigenaarAlreadyExists(Exception):
    pass

class ProceseigenaarNotFound(Exception):
    pass

class InvalidGebruikerOrVernietigingstaak(Exception):
    pass

class Gebruiker:
    def __init__(self, id, naam):
        self.id = id
        self.naam = naam

    def __eq__(self, other):
        if not isinstance(other, Gebruiker):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Vernietigingstaak:
    def __init__(self, id, omschrijving):
        self.id = id
        self.omschrijving = omschrijving

    def __eq__(self, other):
        if not isinstance(other, Vernietigingstaak):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class DestructionTaskService:
    def __init__(self):
        # Key: vernietigingstaak id, value: gebruiker instance
        self._relaties = {}

    def add_proceseigenaar(self, gebruiker, vernietigingstaak):
        if not isinstance(gebruiker, Gebruiker) or not isinstance(vernietigingstaak, Vernietigingstaak):
            raise InvalidGebruikerOrVernietigingstaak()
        taakid = vernietigingstaak.id
        if taakid in self._relaties:
            raise ProceseigenaarAlreadyExists()
        self._relaties[taakid] = gebruiker

    def remove_proceseigenaar(self, gebruiker, vernietigingstaak):
        if not isinstance(gebruiker, Gebruiker) or not isinstance(vernietigingstaak, Vernietigingstaak):
            raise InvalidGebruikerOrVernietigingstaak()
        taakid = vernietigingstaak.id
        if taakid not in self._relaties:
            raise ProceseigenaarNotFound()
        # Alleen de juiste gebruiker mag verwijderd worden
        if self._relaties[taakid] == gebruiker:
            del self._relaties[taakid]
        else:
            raise ProceseigenaarNotFound()

    def is_proceseigenaar(self, gebruiker, vernietigingstaak):
        if not isinstance(gebruiker, Gebruiker) or not isinstance(vernietigingstaak, Vernietigingstaak):
            return False
        taakid = vernietigingstaak.id
        return self._relaties.get(taakid) == gebruiker