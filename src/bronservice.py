from typing import List, Dict

class Bron:
    def __init__(self, name: str, element_type: List[Dict], attributes: List[Dict]):
        self.name = name
        self.element_type = element_type
        self.attributes = attributes

class BronService:
    def create_bron(self, data: Dict) -> Bron:
        name = data.get("name")
        element_type = data.get("element_type", [])
        attributes = data.get("attributes", [])

        if not name:
            raise ValueError("Name is required")

        valid_element_types = {"ObjectType", "Attribute"}
        if any(et["ElementType"] not in valid_element_types for et in element_type):
            raise ValueError("Invalid element type")

        element_ids = set()
        for et in element_type:
            if et["ElementID"] in element_ids:
                raise ValueError("Duplicate ElementID found")
            element_ids.add(et["ElementID"])

        return Bron(name, element_type, attributes)