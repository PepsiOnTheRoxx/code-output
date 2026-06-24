from src.services.createvernietigingstaak_exceptions import (
    DuplicateVernietigingstaakException,
    InvalidVernietigingstaakDataException,
    MissingVernietigingstaakAttributeException
)


class Vernietigingstaak:
    def __init__(self, objecttype_id, attribute_10, attribute_11, attribute_12):
        self.objecttype_id = objecttype_id
        self.attribute_10 = attribute_10
        self.attribute_11 = attribute_11
        self.attribute_12 = attribute_12


class VernietigingstaakService:
    def __init__(self):
        self.vernietigingstaken = []

    def _is_duplicate(self, data):
        for taak in self.vernietigingstaken:
            if (
                taak.objecttype_id == data["objecttype_id"] and
                taak.attribute_10 == data["attribute_10"] and
                taak.attribute_11 == data["attribute_11"] and
                taak.attribute_12 == data["attribute_12"]
            ):
                return True
        return False

    def create_vernietigingstaak(self, data):
        required_attrs = [
            "objecttype_id",
            "attribute_10",
            "attribute_11",
            "attribute_12"
        ]
        for attr in required_attrs:
            if attr not in data:
                raise MissingVernietigingstaakAttributeException(f"Missing attribute: {attr}")

        if not isinstance(data["objecttype_id"], int) or data["objecttype_id"] != 10:
            raise InvalidVernietigingstaakDataException("Invalid objecttype_id")

        if not isinstance(data["attribute_10"], str):
            raise InvalidVernietigingstaakDataException("attribute_10 must be a string")

        if not isinstance(data["attribute_11"], int):
            raise InvalidVernietigingstaakDataException("attribute_11 must be an int")

        if not isinstance(data["attribute_12"], bool):
            raise InvalidVernietigingstaakDataException("attribute_12 must be a bool")

        if self._is_duplicate(data):
            raise DuplicateVernietigingstaakException("Duplicate vernietigingstaak")

        taak = Vernietigingstaak(
            objecttype_id=data["objecttype_id"],
            attribute_10=data["attribute_10"],
            attribute_11=data["attribute_11"],
            attribute_12=data["attribute_12"]
        )
        self.vernietigingstaken.append(taak)
        return taak