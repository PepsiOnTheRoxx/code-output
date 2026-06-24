class Bron:
    def __init__(self, element_type, element_id):
        self.element_type = element_type
        self.element_id = element_id


class BronService:
    def __init__(self):
        self.bronnen = []

    def create_bron(self, element_type, element_id):
        if element_type not in ["ObjectType", "Attribute"]:
            raise ValueError("Invalid element type")
        if not isinstance(element_id, int) or element_id <= 0:
            raise ValueError("Element ID must be a positive integer")

        bron = Bron(element_type, element_id)
        self.bronnen.append(bron)
        return bron

    def read_bron(self, element_id):
        for bron in self.bronnen:
            if bron.element_id == element_id:
                return bron
        raise ValueError("Bron not found")

    def update_bron(self, element_id, new_element_type):
        bron = self.read_bron(element_id)
        if new_element_type not in ["ObjectType", "Attribute"]:
            raise ValueError("Invalid element type")
        bron.element_type = new_element_type

    def delete_bron(self, element_id):
        bron = self.read_bron(element_id)
        self.bronnen.remove(bron)