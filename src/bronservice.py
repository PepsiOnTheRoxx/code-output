class Bron:
    def __init__(self, name, type, attributes):
        self.name = name
        self.type = type
        self.attributes = attributes

class BronService:
    def __init__(self):
        self._brons = []
        self._valid_attributes = {
            "Attribute15": 15,
            "Attribute16": 16
        }

    def create_bron(self, name, type, attributes):
        required_attrs = set(self._valid_attributes.keys())
        if set(attributes.keys()) != required_attrs:
            missing = required_attrs - set(attributes.keys())
            if missing:
                raise ValueError("Missing required attributes")
            invalid = set(attributes.keys()) - required_attrs
            if invalid:
                raise KeyError("Invalid attribute(s)")
        for key in attributes.keys():
            if key not in self._valid_attributes:
                raise KeyError(f"Invalid attribute: {key}")
        bron = Bron(name, type, attributes.copy())
        self._brons.append(bron)
        return bron

    def get_all_brons(self):
        return list(self._brons)