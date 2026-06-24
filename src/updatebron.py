class BronNotFoundException(Exception):
    pass

class InvalidBronDataException(Exception):
    pass

class Bron:
    def __init__(self, bron_id, naam, beschrijving):
        self.bron_id = bron_id
        self.naam = naam
        self.beschrijving = beschrijving

    def update(self, naam=None, beschrijving=None):
        if naam is not None:
            self.naam = naam
        if beschrijving is not None:
            self.beschrijving = beschrijving

class BronRepository:
    def __init__(self):
        self._bronnen = {}

    def get_bron_by_id(self, bron_id):
        return self._bronnen.get(bron_id)

    def save_bron(self, bron):
        self._bronnen[bron.bron_id] = bron

class BronService:
    def __init__(self, repository):
        self.repository = repository

    def update_bron(self, bron_id, naam=None, beschrijving=None):
        bron = self.repository.get_bron_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException(f"Bron with id {bron_id} not found")

        if naam is not None and (not isinstance(naam, str) or not naam.strip()):
            raise InvalidBronDataException("Naam is verplicht en moet een niet-lege string zijn")

        if beschrijving is not None and not isinstance(beschrijving, str):
            raise InvalidBronDataException("Beschrijving moet een string zijn")

        bron.update(naam=naam, beschrijving=beschrijving)
        self.repository.save_bron(bron)
        return bron