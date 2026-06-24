from src.services.broncreate_exceptions import (
    BronCreateInvalidNameException,
    BronCreateInvalidDescriptionException,
    BronCreateDuplicateException,
)

class InvalidBronDataException(Exception):
    pass

class BronAlreadyExistsException(Exception):
    pass

class Bron:
    _id_counter = 1

    def __init__(self, naam, beschrijving):
        self.id = Bron._id_counter
        Bron._id_counter += 1
        self.naam = naam
        self.beschrijving = beschrijving

class BronService:
    def __init__(self):
        self._bronnen = {}

    def create_bron(self, naam, beschrijving):
        if naam is None or beschrijving is None:
            raise InvalidBronDataException()
        if not isinstance(naam, str) or not naam.strip():
            raise InvalidBronDataException()
        if not isinstance(beschrijving, str) or not beschrijving.strip():
            raise InvalidBronDataException()
        if naam in self._bronnen:
            raise BronAlreadyExistsException()
        bron = Bron(naam=naam, beschrijving=beschrijving)
        self._bronnen[naam] = bron
        return bron