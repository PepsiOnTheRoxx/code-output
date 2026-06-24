from src.createbron_exceptions import *

class Bron:
    _id_counter = 1

    def __init__(self, naam, beschrijving):
        self.naam = naam
        self.beschrijving = beschrijving
        self.id = Bron._id_counter
        Bron._id_counter += 1

class BronService:
    def __init__(self):
        self._bronnen_by_naam = {}

    def create_bron(self, naam, beschrijving):
        if naam is None or not str(naam).strip():
            raise InvalidBronNameException()
        if beschrijving is None or not str(beschrijving).strip():
            raise InvalidBronDescriptionException()
        if naam in self._bronnen_by_naam:
            raise BronAlreadyExistsException()
        bron = Bron(str(naam).strip(), str(beschrijving).strip())
        self._bronnen_by_naam[bron.naam] = bron
        return bron