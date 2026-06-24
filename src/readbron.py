class BronNotFoundException(Exception):
    pass

class Bron:
    def __init__(self, bron_id, name, description):
        self.bron_id = bron_id
        self.name = name
        self.description = description

class BronService:
    def __init__(self):
        self.bronnen = {}

    def add_bron(self, bron):
        self.bronnen[bron.bron_id] = bron

    def get_bron(self, bron_id):
        if bron_id in self.bronnen:
            return self.bronnen[bron_id]
        else:
            raise BronNotFoundException(f'Bron with ID {bron_id} not found')

# Voorbeeld gebruik om de functionaliteit te demonstreren
if __name__ == "__main__":
    bron_service = BronService()
    bron_service.add_bron(Bron(1, "Bron 1", "Beschrijving van Bron 1"))
    bron_service.add_bron(Bron(2, "Bron 2", "Beschrijving van Bron 2"))

    try:
        bron = bron_service.get_bron(1)
        print(f'Gevonden bron: {bron.name} - {bron.description}')
    except BronNotFoundException as e:
        print(e)