class BronService:
    class Bron:
        def __init__(self, naam, beschrijving):
            self.naam = naam
            self.beschrijving = beschrijving

    class InvalidBronException(Exception):
        pass

    def create_bron(self, naam, beschrijving):
        if not naam or not beschrijving:
            raise self.InvalidBronException("Naam en beschrijving moeten ingevuld zijn.")
        return self.Bron(naam, beschrijving)