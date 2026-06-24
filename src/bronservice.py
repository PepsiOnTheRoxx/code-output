class Bron:
    def __init__(self, name, element_type, attributes):
        self.name = name
        self.element_type = element_type
        self.attributes = attributes

class BronService:
    valid_element_types = {"ObjectType", "Attribute"}

    def create_bron(self, data):
        name = data.get("name")
        element_type = data.get("element_type", [])
        attributes = data.get("attributes", [])

        if not name:
            raise ValueError("Name is required")

        self.validate_element_types(element_type)

        if self.has_duplicate_element_id(element_type):
            raise ValueError("Duplicate ElementID found")

        return Bron(name, element_type, attributes)

    def validate_element_types(self, element_types):
        for elem in element_types:
            if elem["ElementType"] not in self.valid_element_types:
                raise ValueError("Invalid element type")

    def has_duplicate_element_id(self, element_types):
        seen_ids = set()
        for elem in element_types:
            elem_id = elem["ElementID"]
            if elem_id in seen_ids:
                return True
            seen_ids.add(elem_id)
        return False