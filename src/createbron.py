class BronNotFoundException(Exception):
    pass

class Bron:
    def __init__(self, element_id, attributes):
        self.element_id = element_id
        self.attributes = attributes

class BronService:
    def __init__(self):
        self.brons = {}

    def create_bron(self, element_id, attributes):
        if element_id in self.brons:
            raise ValueError("Bron with this ID already exists.")
        bron = Bron(element_id, attributes)
        self.brons[element_id] = bron
        return bron.attributes

    def get_bron(self, element_id):
        if element_id not in self.brons:
            return None
        return self.brons[element_id].attributes

    def update_bron(self, element_id, attributes):
        if element_id not in self.brons:
            raise ValueError("Bron not found.")
        self.brons[element_id].attributes = attributes

    def delete_bron(self, element_id):
        if element_id not in self.brons:
            raise ValueError("Bron not found.")
        del self.brons[element_id]