from src.services.createbron_exceptions import BronAlreadyExistsException, InvalidBronDataException

class BronAttribute:
    def __init__(self, attribute_id, value):
        self.attribute_id = attribute_id
        self.value = value

class Bron:
    def __init__(self, element_type, element_id, attributes):
        self.element_type = element_type
        self.element_id = element_id
        self.attributes = attributes

class BronService:
    _valid_element_type = "ObjectType"
    _valid_element_id = 12
    _valid_attribute_ids = {15, 16}

    def __init__(self):
        self._bron_storage = []

    def bron_exists(self, bron_data):
        for bron in self._bron_storage:
            if bron.element_type == bron_data.get("ElementType") and bron.element_id == bron_data.get("ElementID"):
                return True
        return False

    def create_bron(self, bron_data):
        if not isinstance(bron_data, dict):
            raise InvalidBronDataException("bron_data must be a dict")
        element_type = bron_data.get("ElementType")
        element_id = bron_data.get("ElementID")
        attributes = bron_data.get("attributes")

        if element_type != self._valid_element_type or element_id != self._valid_element_id:
            raise InvalidBronDataException("Invalid ElementType or ElementID")
        if attributes is None or not isinstance(attributes, list) or len(attributes) == 0:
            raise InvalidBronDataException("Attributes missing or empty")
        attribute_ids = set()
        bron_attributes = []
        for attr in attributes:
            attribute_id = attr.get("AttributeID")
            value = attr.get("value")
            if attribute_id not in self._valid_attribute_ids:
                raise InvalidBronDataException(f"Invalid AttributeID: {attribute_id}")
            attribute_ids.add(attribute_id)
            bron_attributes.append(BronAttribute(attribute_id, value))
        if not self._valid_attribute_ids.issubset(attribute_ids):
            raise InvalidBronDataException("Missing required AttributeID(s)")
        if self.bron_exists(bron_data):
            raise BronAlreadyExistsException("Bron already exists")
        bron = Bron(element_type, element_id, bron_attributes)
        self._bron_storage.append(bron)
        return bron