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
        return bron

    def get_bron(self, element_id):
        if element_id not in self.brons:
            raise BronNotFoundException("Bron not found.")
        return self.brons[element_id]

    def update_bron(self, element_id, attributes):
        if element_id not in self.brons:
            raise BronNotFoundException("Bron not found.")
        self.brons[element_id].attributes = attributes

    def delete_bron(self, element_id):
        if element_id not in self.brons:
            raise BronNotFoundException("Bron not found.")
        del self.brons[element_id]

# Implementing a simple test just to demonstrate functionality
if __name__ == "__main__":
    service = BronService()
    attributes = [{"ElementType": "Attribute", "ElementID": 15}, {"ElementType": "Attribute", "ElementID": 16}]
    bron = service.create_bron(12, attributes)

    print("Created Bron:", bron.element_id, bron.attributes)  # To verify creation
    fetched_bron = service.get_bron(12)
    print("Fetched Bron:", fetched_bron.element_id, fetched_bron.attributes)  # To verify fetching

    service.update_bron(12, [{"ElementType": "Attribute", "ElementID": 20}])
    updated_bron = service.get_bron(12)
    print("Updated Bron:", updated_bron.element_id, updated_bron.attributes)  # Verify update

    service.delete_bron(12)
    try:
        service.get_bron(12)  # Should raise exception
    except BronNotFoundException as e:
        print(e)  # To verify deletion