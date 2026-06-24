class Bron:
    def __init__(self, name, type, attributes):
        self.name = name
        self.type = type
        self.attributes = attributes

    def __eq__(self, other):
        if isinstance(other, Bron):
            return (
                self.name == other.name and
                self.type == other.type and
                self.attributes == other.attributes
            )
        return False

class BronService:
    VALID_ATTRIBUTES = {
        "Attribute15": 15,
        "Attribute16": 16
    }

    REQUIRED_ATTRIBUTES = set(VALID_ATTRIBUTES.keys())

    def __init__(self):
        self._brons = []

    def create_bron(self, name, type, attributes):
        # Check that all required attributes are present
        if set(attributes.keys()) != self.REQUIRED_ATTRIBUTES:
            raise ValueError("Missing required attribute(s)")

        # Check that all supplied attribute keys are valid
        for key in attributes:
            if key not in self.VALID_ATTRIBUTES:
                raise KeyError(f"Attribute '{key}' is invalid.")

        bron = Bron(name, type, attributes.copy())
        self._brons.append(bron)
        return bron

    def get_all_brons(self):
        return self._brons.copy()