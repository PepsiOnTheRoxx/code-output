class BronNotFoundException(Exception):
    pass

class BronService:
    def __init__(self):
        self.bronnen = {
            12: {"naam": "Basis Bron", "type": "Watertype", "locatie": "Nederland"}
        }

    def read_bron(self, element_id):
        if element_id not in self.bronnen:
            raise BronNotFoundException(f"Bron met ID {element_id} niet gevonden.")
        return self.bronnen[element_id]